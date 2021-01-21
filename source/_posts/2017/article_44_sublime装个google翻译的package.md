
---
title: sublime装个google翻译的package
catalog: true
date: 2017-11-26 13:25:56
---

原以为翻译这种包package control就可以解决，还是有许多问题出现，所以记录一下。顺便了解一下sublime包文件结构，毕竟也是python写的！<!--more-->

这里引用的是github上的一个<a href="https://github.com/mullnerz/SublimeText-Google-Translate-Plugin">google 翻译包</a>，这是另一个人改过的，主要更新了google的api，他的原作是在<a href="https://github.com/MTimer/SublimeText-Google-Translate-Plugin">这里</a>。

这里的操作皆为windows平台下，首先用git
<pre><code>git clone https://github.com/MTimer/SublimeText-Google-Translate-Plugin 'Inline Google Translate'</code></pre>
打开sublime，点击preferences-&gt;browse packages。把clone下来的文件复制到这里，文件名必须为 Inline Google Translate。

直接使用当然还会有问题，这里首先是使用代理的问题，由于gwf，需要通过代理来访问google api。因此在preferences-&gt;package setting-&gt;google translate-&gt;setting user中，添加以下，proxy部分添加自己电脑使用的代理的协议和端口，这里使用的是shadowsocks的默认的http和端口。
<pre>{     
    "source_language": "", // 默认是 '自动检测'
    "target_language": "zh-CN", // 默认是 en  英文
    "target_type": "html",  // 输出格式，plain 或者 html 格式
    "proxy_enable": "yes",  // 开启或关闭代理
    "proxy_type": "http", // socks4 或者 socks5 或者 http
    "proxy_host": "127.0.0.1",  // 比如 127.0.0.1
    "proxy_port": "1080"    // 比如 9050
}</pre>
到这里可以尝试选中一行单词，按下ctrl+alt+g，如果有效果，则前面部分完成了；如果没效果，则按ctrl+~看命令行输出的错误。

这个包还有另一个问题就是如果选择多行只会翻译第一行。因此对其中的python代码做一定的修改。在goTranslate.py 第一个run函数部分
<pre>def run(self, edit, proxy_enable = settings.get("proxy_enable"), proxy_type = settings.get("proxy_type"), proxy_host = settings.get("proxy_host"), proxy_port = settings.get("proxy_port"), source_language = settings.get("source_language"), target_language = settings.get("target_language")):
        if not source_language:
            source_language = settings.get("source_language")
        if not target_language:
            target_language = settings.get("target_language")
        if not proxy_enable:
            proxy_enable = settings.get("proxy_enable")
        if not proxy_type:
            proxy_type = settings.get("proxy_type")
        if not proxy_host:
            proxy_host = settings.get("proxy_host")
        if not proxy_port:
            proxy_port = settings.get("proxy_port")
        target_type = settings.get("target_type")

        for region in self.view.sel():
            if not region.empty():

                v = self.view
                selection = v.substr(region).encode('utf-8')
                print(selection)
                translate = GoogleTranslate(proxy_enable, proxy_type, proxy_host, proxy_port, source_language, target_language)
                #主要改了这下面部分，使用分行获取翻译结果并合并
                tmp=[]
                if not target_language:
                    self.view.run_command("go_translate_to")
                    return                          
                else:
                    for line in selection.split(b"\n"):
                        tmp.append(translate.translate(line, target_type))
                    result="\n".join(tmp)

                v.replace(edit, region, result)
                if not source_language:
                    detected = 'Auto'
                else:
                    detected = source_language
                sublime.status_message(u'Done! (translate '+detected+' --&gt; '+target_language+')')</pre>
完成保存sublime就会自动重新加载包。

之后再可以试试多行的效果。

另外插一个就是快捷键，由于这里的ctrl+alt+g一般一只手操作不来，所以也想自定义一下。

以文本的形式打开同目录下的Default (Windows).sublime-keymap。改第一个keys的内容便是修改快捷键，我这里修改为了ctrl+alt+z，因为ctrl+z可以回撤一步，两个便可以配合使用。

这里涉及到了sublime包的一些编写和使用，感觉也并不是十分复杂，必要也可以自己写个！
