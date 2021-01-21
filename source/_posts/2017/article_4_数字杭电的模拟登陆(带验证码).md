
---
title: 数字杭电的模拟登陆(带验证码)
catalog: true
date: 2017-3-8 13:11:21
---

对于一个学生，研究学校网站还是比较有趣滴！

Talk is cheap！Then I show the code.

下面是用php的实现，具体细节在注释里讲解<!--more-->
<pre>//登录之前先获取cookie及lt(一次性使用，lt很关键)
function GetCookie(){
    //cookie的地址
    $cookie=dirname(__FILE__).'/cookie.txt';
    //curl来模拟登陆一次教务网站获取返回的页面代码
    $ch = curl_init(); 
    curl_setopt($ch, CURLOPT_URL, 'http://cas.hdu.edu.cn/cas/login'); 
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_COOKIEJAR, $cookie);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $res=curl_exec($ch);
    curl_close($ch);
    //用正则匹配到代码里的lt存起来
    $preg = '|&lt;input type="hidden" name="lt" value=[\"](.*?)[\"] /&gt;|U';
    preg_match_all($preg, $res, $arr); 
    $lt=$arr[1][0];
    //把lt存在session里
    $_SESSION['lt']=$lt;
    //带着刚才的cookie在curl一次验证码的网站得到验证码图片
    $ch = curl_init(); 
    curl_setopt($ch, CURLOPT_URL, 'http://cas.hdu.edu.cn/cas/Captcha.jpg'); 
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_COOKIEFILE, $cookie);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $data=curl_exec($ch);
    curl_close($ch);
    //获取时间(为确保验证码唯一性)
    $time=time();
    //把验证码保存成jpg
    file_put_contents(dirname(__FILE__).'/yzm/'.$time.'.jpg',$data);
    //为了方便这里返回时间
    return $time;
 }</pre>
<pre>//验证是否登录成功
function VerLogin($username,$password,$yzm){
    //cookie路径
    $cookie=dirname(__FILE__).'/cookie.txt';
    //获取在session里的lt
    $lt=$_SESSION['lt'];
    //构造post内容
    $post_data=array(
        'encodedService'=&gt;'http%3a%2f%2fi.hdu.edu.cn%2fdcp%2findex.jsp',
        'service'=&gt;'http://i.hdu.edu.cn/dcp/index.jsp',
        'serviceName'=&gt;'null',
        'loginErrCnt'=&gt;'0',
        'username'=&gt;$username,
        'password'=&gt;md5($password),
        'lt'=&gt;$lt,
        'captcha'=&gt;$yzm
     );
    //带着cookie模拟登陆(为了防止被认出来构造的比较完整，嘻嘻)
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, "http://cas.hdu.edu.cn/cas/login");
    curl_setopt($curl, CURLOPT_HEADER, 0);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($curl,CURLOPT_REFERER,'http://cas.hdu.edu.cn/cas/login?service=http%3A%2F%2Fi.hdu.edu.cn%2Fdcp%2Findex.jsp');
    curl_setopt($curl, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'); 
    curl_setopt($curl, CURLOPT_POST, 1);
    curl_setopt($curl, CURLOPT_COOKIEFILE, $cookie);
    curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($post_data));
    curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1); 
    $res=curl_exec($curl);
    curl_close($curl);
    //得到一个自带跳转的页面的代码(跳转过去就是登陆后的主页面了哦)
    //用正则匹配跳转，如果有则返回成功，没则返回失败
    preg_match_all('/window.location.href=[\"](.*)[\"]/i', $res, $results);
    if($results[1][0]==null){
        return false;
    }else{
        return true;
    }
 }</pre>
<pre>//使用函数
//获取cookie
$time=GetCookie();
//下面是验证码图片路径，根据图片得到正确验证码
//$Imgdir=dirname(__file__)."/yzm/".$time.".jpg";
//根据得到的验证码加上学号密码登录
$stuid="15******";
$password="********";
$yzm="****";
if(VerLogin($stuid,$password,$yzm)){
    echo "登录成功";
}else{
    echo "登录失败";
}</pre>
个人推荐使用的是fiddler来抓包，其他的网页的登陆也可以用相同的思路来研究。
