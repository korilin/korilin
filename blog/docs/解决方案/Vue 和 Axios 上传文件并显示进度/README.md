---
title: Vue 和 Axios 上传文件并显示进度
date: 2020-3-15
categories: 解决方案
tags:
    - Vue
    - Axios
---

在前端和后端分离的情况下，我们可以使用 Axios 的方式来发送请求获取数据，通过 Vue 来修改页面的内容

同时我们也可以提交表单上传文件到服务器进行存储

开始前要先引入 Vue.js 和 Axios, 这里使用 CDN 引入

```Html
<body>
    <script src="https://cdn.jsdelivr.net/npm/vue"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</body>
```

<!-- more -->

### [建立表单](#建立表单)

假如我们有一个简单的的上传表单是这样的

```Html
<form id="upload">
    <input type="file" ref="file">
    <input type="submit" value="上传">
</form>
```

在 Vue 中，我们首先要建立和表单的关联

```JavaScript
var upload = new Vue({
    el: "#upload",
    data: {
    }
})
```

接下来，我们需要在 Vue 中获取到上传的问题，所以我们可以在 Vue 中定一个存放文件的变量 file, 给`input[type="file]"`定义一个修改事件，每次选择文件就修改 file 这个变量

于是，我们的代码就变成了这样

```JavaScript
var upload = new Vue({
    el: "#upload",
    data: {
        file: ""
    },
    methods: {
        changeFile: function (e) {
            this.file = e.target.files[0];
        }
    }
})
```

在这里 changeFile 可以将传入的 DOM 元素的文件赋值给 Vue 中的 file, 然后把这个函数绑定到 input 的修改事件里

```Html
<form id="upload">
    <input type="file" ref="file" @change="changeFile($event)">
    <input type="submit" value="上传">
</form>
```

这样我们每次选择文件后，Vue 里面的 file 值就会变成这个文件的对象，接下来可以写上传功能了，我们要用 Axios 来发送携带文件的请求，所以我们要在 Vue 里面写一个函数，然后把这个函数绑定到表单的提交事件里

### [上传文件](#上传文件)

我们在写的时候需要定义参数，请求配置，然后和请求地址一起传入，这样就不容易出现错误

参数使用`append`传入键值对，配置里面要表面请求体的格式是`multipart/form-data`

```JavaScript
var upload = new Vue({
    el: "#upload",
    data: {
        file: ""
    },
    methods: {
        changeFile: function (e) {
            this.file = e.target.files[0];
        }
    },
    upload: function () {
        var that = this;
        let param = new FormData();
        param.append('file', that.file);
        let config = {
            headers: { "Content-Type": "multipart/form-data" }
        }
        axios
            .post("upload", param, config) //upload是我在这个页面的地址的相对路径下的请求地址
            .then(response => {
                // 成功处理
            })
            .catch(error => {
                // 失败处理
            })
    }
})
```

```Html
<form id="upload" @submit="upload">
    <input type="file" ref="file" @change="changeFile($event)">
    <input type="submit" value="上传">
</form>
```

### [页面处理](#页面处理)

做到这一步其实已经可以上传文件了，但是通常我们的页面上传文件时会有很多需要展示的内容，例如展示上传进度，在不刷新页面的情况下提示上传成功，或者判断用户上传时是否选择了文件，所以我们要对代码进一步修改

在 @submit 后面加上 prevent 可以阻止表单提交时页面刷新，然后定义一些默认不显示的标签来展示上传时和上传后的消息

```Html
<input type="file" ref="file" @change="changeFile($event)">
<button type="submit" @click="upload">上传</button>
<!-- 上传信息 -->
<p style="font-size: 14px;color: rgb(21, 146, 196);" v-show="percentage==0?false:(percentage==100?false:true)">{{percentage}}%</p>
<p style="font-size: 14px;color: green;" v-show="mseshow">{{mes}}</p>
<p style="font-size: 14px;color: red;" v-show="errshow">{{mes}}</p>
```

在 Axios 中，我们可以通过 axios 发送请求时 config 里的`onUploadProgress`函数来获取上传进度，修改完的代码如下：

```JavaScript
var upload = new Vue({
    el: "#upload",
    data: {
        file: "",
        percentage: 0,
        mseshow: false,
        errshow: false,
        mes: ""
    },
    methods: {
        changeFile: function (e) {
            this.file = e.target.files[0];
        }
    },
    upload: function () {
        var that = this;
        if (that.file == "") {
            that.mes = "请选择文件";
            that.errshow = true;
        } else {
            that.errshow = false;
            let param = new FormData();
            param.append('file', that.file);
            let config = {
                onUploadProgress: progressEvent => {
                    //progressEvent.loaded:已上传文件大小
                    //progressEvent.total:被上传文件的总大小
                    that.percentage = (progressEvent.loaded / progressEvent.total).toFixed(2) * 100;
                },
                headers: { "Content-Type": "multipart/form-data" }
            }
            axios
                .post("upload", param, config) //upload是我在这个页面的地址的相对路径下的请求地址
                .then(response => {
                    // 成功处理
                    that.mseshow = true;
                    that.mes = "上传成功";
                })
                .catch(error => {
                    // 失败处理
                    that.errshow = true;
                    that.mes = "上传失败";
                    // 提示报错内容
                    alert(error);
                })
        }
    }
})
```

这样就可以实现用 Vue 和 Axios 来上传文件并在页面不刷新的情况下显示上传信息了

### [参考](#参考)

- Vue.js 官网：<https://cn.vuejs.org/>
- Axios 文档：<https://github.com/axios/axios>
