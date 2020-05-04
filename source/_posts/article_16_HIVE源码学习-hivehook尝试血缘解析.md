---
title: HIVE源码学习-hivehook尝试表血缘与字段血缘的解析
catalog: true
date: 2020-05-04 14:31:43
subtitle: 
header-img: 
tags:
- HIVE
---


## 前言

hook在中间执行过程中留下不少钩子可以供开发者开发拓展功能，大致有如下几个

- driver run的时候

- 执行计划semanticAnalyze前后

- 查询放入job之前

- exec前后，失败时

下面引用一份完整的hook的流程，包括相应的配置项。

``` java
Driver.run()

=> HiveDriverRunHook.preDriverRun()(hive.exec.driver.run.hooks)

=> Driver.compile()

=> HiveSemanticAnalyzerHook.preAnalyze()(hive.semantic.analyzer.hook)

=> SemanticAnalyze(QueryBlock, LogicalPlan, PhyPlan, TaskTree)

=> HiveSemanticAnalyzerHook.postAnalyze()(hive.semantic.analyzer.hook)

=> QueryString redactor(hive.exec.query.redactor.hooks)

=> QueryPlan Generation

=> Authorization

=> Driver.execute()

=> ExecuteWithHookContext.run() || PreExecute.run() (hive.exec.pre.hooks)

=> TaskRunner

=> if failed, ExecuteWithHookContext.run()(hive.exec.failure.hooks)

=> ExecuteWithHookContext.run() || PostExecute.run() (hive.exec.post.hooks)

=> HiveDriverRunHook.postDriverRun()(hive.exec.driver.run.hooks)
```

## 血缘解析


### 表血缘

``` java
package cn.ganjiacheng;

import org.apache.hadoop.hive.ql.hooks.ExecuteWithHookContext;
import org.apache.hadoop.hive.ql.hooks.HookContext;
import org.apache.hadoop.hive.ql.hooks.LineageInfo;
import org.apache.hadoop.hive.metastore.api.Table;

import java.util.*;

/**
 * @description:
 * @author: again
 * @email: ganjiacheng@souche.com
 * @date: 2020/5/4 3:18 下午
 */
public class MyLineagehook implements ExecuteWithHookContext {

    private Set<String> inputTables = new HashSet<>();

    private Set<String> outputTables = new HashSet<>();

    private String dealOutputTable(Table table) {
        String dbName = Optional.ofNullable(table).map(Table::getDbName).orElse(null);
        String tableName = Optional.ofNullable(table).map(Table::getTableName).orElse(null);
        if(tableName == null) {
            return null;
        }
        return dbName != null ? String.format("%s.%s", dbName, tableName) : tableName;
    }

    @Override
    public void run(HookContext hookContext) throws Exception {
        for(Map.Entry<LineageInfo.DependencyKey, LineageInfo.Dependency> dep: hookContext.getLinfo().entrySet()){
            Optional.ofNullable(dep.getKey())
                    .map(LineageInfo.DependencyKey::getDataContainer)
                    .map(LineageInfo.DataContainer::getTable)
                    .map(this::dealOutputTable)
                    .ifPresent(outputTables::add);
            Optional.ofNullable(dep.getValue())
                    .map(LineageInfo.Dependency::getBaseCols)
                    .ifPresent(items -> {
                        items.stream().map(LineageInfo.BaseColumnInfo::getTabAlias)
                                .map(LineageInfo.TableAliasInfo::getTable)
                                .map(this::dealOutputTable)
                                .forEach(inputTables::add);
                    });
        }
        System.out.println(inputTables);
        System.out.println(outputTables);
    }

}
```

### 字段血缘




