<style>
h1{text-align:center; /*author:ningci dev date:2017-04-27 22:21*/}
*{background-color:#000; color:#fff;}
pre{margin:10px;padding:10px;border:1px solid #00f; color:#f6c608;}
</style>
<h1>real time network status !</h1>
<h3>day</h3>
<pre>
<?php
echo system("vnstat -d");
?>
</pre>
<h3>hour</h3>
<pre>
<?php
echo system("vnstat -h");
?>
</pre>

<h3>month</h3>
<pre>
<?php
echo system("vnstat -m");
?>
</pre>
