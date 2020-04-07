---
title: '基于antlr4实现HQL的解析[元数据]'
catalog: true
date: 2020-04-07 15:24:40
subtitle: 
header-img: "/img/article_header/header.jpg"
tags:
- HQL解析
- 元数据
- Java
---

## 前言

在大数据场景中，HQL的使用次数很多：离线任务，及时查询，数仓建模等。 

关于HQL解析在hive底层也有他自己的HQL解析实现。不过底层的实现直接用不起来，这边使用antlr4直接来实现HQL的解析。

HQL解析在很多场景能用到并发挥如虎添翼的作用，这边开个新坑，会分好几个文章来讲主要用到的一些场景和实现。  

本文主要讲CREATE语句解析出元数据。会用到的场景也很多，比如建模的时候，离线任务中的创表和其他有用到类似建表的地方都可以转换为HQL的交互方式拿到数据，而不是传统的填写表单。

## 前期准备

- antlr4安装看[这里官方教程](https://www.antlr.org/) 
- idea的插件 ANTLR v4 grammar plugin
- sql的解析文件 [Hplsql.g4](https://github.com/apache/hive/blob/master/hplsql/src/main/antlr4/org/apache/hive/hplsql/Hplsql.g4)(这个文件大部分解析都有了，不过还有很多可以改进的)

起个java项目，加上dependency antlr4-runtime 和    
plugin antlr4-maven-plugin(可以在编译的时候将g4
文件生成lexer和parser等文件)

## 具体实现

antlr4支持两种格式listener和visitor遍历模式。两种模式的具体用法和区别看[这里](https://abcdabcd987.com/notes-on-antlr4/)。  
这边以visitor模式实现。

### g4分析

hplsql.g4文件中创表语句相关的主要为下面一些
```
// 创表语句入口 (create ... 表名 表来源)
create_table_stmt :
       T_CREATE (T_EXTERNAL)? T_TABLE (T_IF T_NOT T_EXISTS)? table_name create_table_definition
     ;

// 创表来源，这边用的是是字段和表其他配置 
// (... 字段 ... 表配置)
create_table_definition :
      (T_AS? T_OPEN_P select_stmt T_CLOSE_P | T_AS? select_stmt | T_OPEN_P create_table_columns T_CLOSE_P | T_LIKE table_name) create_table_options?
     ;

// 每个字段 (字段名 类型 长度 ... 备注)
create_table_columns_item :
       column_name dtype dtype_len? dtype_attr* create_table_column_inline_cons* (T_COMMENT column_comment)?
     | (T_CONSTRAINT ident)? create_table_column_cons
     ;

// 表其他相关配置 (备注 分区 行格式 存储类型 存储位置 表属性)
create_table_options_hive_item :
    (T_COMMENT string)?
    create_table_hive_partitioned_by_clause?
    create_table_hive_row_format?
    create_table_hive_stored?
    create_table_hive_location?
    create_table_hive_tblproperties?
     ;
```

### 表字段相关定义

``` java
public class HiveFieldMetadata {
    /**
     * 字段名
     */
    private String fieldName;

    /**
     * 数据类型
     */
    private String dataType;

    /**
     * 字段备注
     */
    private String fieldComment;
}
```

表相关定义

``` java
public class HiveTableMetadata {
    /**
     * 库名
     */
    private String dbName;

    /**
     * 表名
     */
    private String tableName;

    /**
     * 表类型
     */
    private String tableType;

    /**
     * 备注
     */
    private String tableComment;

    /**
     * 分区
     */
    private String partition;

    /**
     * 行格式
     */
    private String rowFormat;

    /**
     * 存储格式
     */
    private String store;

    /**
     * 存储位置
     */
    private String location;

    /**
     * 属性(压缩格式)
     */
    private String properties;

    /**
     * 字段
     */
    private List<HiveFieldMetadata> fields;
}
```

### 源码实现说明

``` java
public class HiveSQLTableMetadata extends HplsqlBaseVisitor {

    private HiveTableMetadata tableMetadata = new HiveTableMetadata();

    private String sourceSQL;

    // 保存原始sql
    public HiveSQLTableMetadata(String sql) {
        this.sourceSQL = sql;
    }

    // 截取原始sql
    private String subSourceSql(ParserRuleContext parserRuleContext) {
        return sourceSQL.substring(
                parserRuleContext.getStart().getStartIndex(),
                parserRuleContext.getStop().getStopIndex() + 1);
    }

    // 处理备注中的引号
    private String dealComment(String comment) {
        if(comment != null && comment.length() >= 2
                && comment.startsWith("\'") && comment.endsWith("\'")){
            comment = comment.substring(1, comment.length()-1);
        }
        return comment;
    }

    // 处理表名字段名中的``
    private String dealNameMark(String name) {
        if(name.startsWith("`") && name.endsWith("`")) {
            return name.substring(1, name.length()-1);
        }else{
            return name;
        }
    }

    // 获取到字段信息
    private void setTableField(HplsqlParser.Create_table_stmtContext ctx) {
        List<HplsqlParser.Create_table_columns_itemContext> itemContexts =
                ctx.create_table_definition().create_table_columns().create_table_columns_item();
        List<HiveFieldMetadata> fields = new ArrayList<>();
        itemContexts.forEach(item -> {
            HiveFieldMetadata field = new HiveFieldMetadata();
            field.setFieldName(Optional.of(item)
                    .map(HplsqlParser.Create_table_columns_itemContext::column_name)
                    .map(RuleContext::getText)
                    .map(this::dealNameMark)
                    .orElse(null));
            String type = Optional.of(item)
                    .map(HplsqlParser.Create_table_columns_itemContext::dtype)
                    .map(RuleContext::getText)
                    .orElse(null);
            String typeLen = Optional.of(item)
                    .map(HplsqlParser.Create_table_columns_itemContext::dtype_len)
                    .map(RuleContext::getText)
                    .orElse("");
            field.setDataType(type != null ? type + typeLen : null);
            field.setFieldComment(Optional.of(item)
                    .map(HplsqlParser.Create_table_columns_itemContext::column_comment)
                    .map(RuleContext::getText)
                    .map(this::dealComment)
                    .orElse(null));
            fields.add(field);
        });
        tableMetadata.setFields(fields);
    }

    // 获取表其他属性信息
    private void setTableOption(HplsqlParser.Create_table_stmtContext ctx) {
        HplsqlParser.Create_table_options_hive_itemContext tableOption =
                ctx.create_table_definition().create_table_options().create_table_options_hive_item();
        tableMetadata.setTableComment(Optional.ofNullable(tableOption)
                .map(HplsqlParser.Create_table_options_hive_itemContext::string)
                .map(RuleContext::getText)
                .map(this::dealComment)
                .orElse(null));
        tableMetadata.setPartition(Optional.ofNullable(tableOption)
                .map(HplsqlParser.Create_table_options_hive_itemContext::create_table_hive_partitioned_by_clause)
                .map(this::subSourceSql)
                .orElse(null));
        tableMetadata.setRowFormat(Optional.ofNullable(tableOption)
                .map(HplsqlParser.Create_table_options_hive_itemContext::create_table_hive_row_format)
                .map(this::subSourceSql)
                .orElse(null));
        tableMetadata.setStore(Optional.ofNullable(tableOption)
                .map(HplsqlParser.Create_table_options_hive_itemContext::create_table_hive_stored)
                .map(this::subSourceSql)
                .orElse(null));
        tableMetadata.setLocation(Optional.ofNullable(tableOption)
                .map(HplsqlParser.Create_table_options_hive_itemContext::create_table_hive_location)
                .map(this::subSourceSql)
                .orElse(null));
        tableMetadata.setProperties(Optional.ofNullable(tableOption)
                .map(HplsqlParser.Create_table_options_hive_itemContext::create_table_hive_tblproperties)
                .map(this::subSourceSql)
                .orElse(null));
    }

    // 执行入口，重写visit create表
    // 获取到表相关信息
    @Override
    public Object visitCreate_table_stmt(HplsqlParser.Create_table_stmtContext ctx) {
        List<ParseTree> tbNameTree = ctx.table_name().ident().children;
        if(tbNameTree.size() == 3 && tbNameTree.get(1).getText().equals(".")) {
            tableMetadata.setDbName(tbNameTree.get(0).getText());
            tableMetadata.setTableName(dealNameMark(tbNameTree.get(2).getText()));
        }else{
            tableMetadata.setTableName(dealNameMark(tbNameTree.get(0).getText()));
        }
        tableMetadata.setTableType(Optional.of(ctx)
                .map(HplsqlParser.Create_table_stmtContext::T_EXTERNAL)
                .map(ParseTree::getText)
                .orElse(null));
        setTableField(ctx);
        setTableOption(ctx);
        return super.visitCreate_table_stmt(ctx);
    }

    // 获取全部创表信息
    public HiveTableMetadata getTableMetadata() {
        return this.tableMetadata;
    }

}
```

### 调用实现

``` java
// 获取解析树
private ParseTree getParseTree(String sourceSQL) {
    CharStream input = CharStreams.fromString(sourceSQL);
    HplsqlLexer lexer = new HplsqlLexer(input);
    CommonTokenStream tokenStream = new CommonTokenStream(lexer);
    HplsqlParser parser = new HplsqlParser(tokenStream);
    return parser.program();
}

// 解析
public HiveTableMetadata getHiveTableMetadata() {
    HiveSQLTableMetadata visitor = new HiveSQLTableMetadata(sourceSQL);
    visitor.visit(getParseTree(sourceSQL));
    return visitor.getTableMetadata();
}
```
