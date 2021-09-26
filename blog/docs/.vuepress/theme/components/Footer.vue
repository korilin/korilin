<template>
    <footer id="footer">
        <div class="content">
            <div>© Copyright <strong>Kori Lin</strong></div>
            <div>
                Powered by
                <a href="https://vuepress.vuejs.org/">Vuepress</a>
            </div>
            <div>
                备案号：<a
                    target="_blank"
                    rel="noopener"
                    href="http://beian.miit.gov.cn/"
                    data-v-882df4f6=""
                >
                    粤ICP备19149652号
                </a>
            </div>
        </div>
    </footer>
</template>

<script>
export default {};
</script>

<style lang="stylus" scoped>
#footer {
    background: #fff;
    box-shadow: 0px 0px 12px 0px #0000001a;
    padding: 30px 0;
    color: #222222;
    font-size: 14px;

    .content {
        width: 80%;
        max-width: 960px;
        margin: auto;

        div {
            margin-top: 5px;
        }
    }
}
</style>