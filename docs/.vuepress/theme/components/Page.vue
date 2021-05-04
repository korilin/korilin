<template>
    <main class="page">
        <slot name="top" />
        <template v-if="this.$route.path == '/'">
            <Home />
        </template>
        <template v-else-if="this.$route.path == '/archive/'">
            <Archive class="theme-default-content" />
        </template>
        <template v-else-if="this.$route.path == '/about/'">
            <Content class="theme-default-content" />
        </template>
        <template v-else>
            <div class="theme-default-content">
                <div class="getback">
                    <router-link to="/archive/"> < 返回 </router-link>
                </div>
                <div class="head">
                    <div class="title">
                        <h1>{{ this.$page.title }}</h1>
                    </div>
                    <div class="info">
                        <span>{{ getDate(this.$page.frontmatter.date) }}</span>
                        <span style="margin-left: 20px">{{
                            this.$page.frontmatter.category
                        }}</span>
                    </div>
                </div>
                <Content />
                <div id="gitalk-container"></div>
            </div>
        </template>

        <PageEdit />

        <PageNav v-bind="{ sidebarItems }" />

        <slot name="bottom" />
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
    </main>
</template>

<script>
import PageEdit from "@theme/components/PageEdit.vue";
import PageNav from "@theme/components/PageNav.vue";
import Archive from "./Archive";
import Home from "./Home";
import "gitalk/dist/gitalk.css";
import Gitalk from "gitalk";

export default {
    components: { PageEdit, PageNav, Archive, Home },
    props: ["sidebarItems"],
    mounted() {
        var gitalk = new Gitalk({
            clientID: "b7aa589ca8f3de3b34fc",
            clientSecret: "9aed479aabee6e5cf3843b672f33c989deb3d83a",
            repo: "https://github.com/korilin/korilin",
            owner: "korilin",
            admin: [
                "korilin",
            ],
            id: location.pathname, // Ensure uniqueness and length less than 50
            distractionFreeMode: false, // Facebook-like distraction free mode
        });

        gitalk.render("gitalk-container");
    },
    methods: {
        getDate(date) {
            var d = new Date(date);
            var year = d.getFullYear();
            var month = d.getMonth() + 1;
            var day = d.getDate();
            return year + "年" + month + "月" + day + "日";
        },
    },
};
</script>

<style lang="stylus" scoped>
.page {
    padding-bottom 2rem
    display block

    .head {
        border-top 1px solid #27282c33
        border-bottom 1px solid #27282c33
        padding 30px 0
        margin-bottom 20px
    }

    .title {
        text-align center
    }

    .info {
        text-align center
        color #27282cbf
        font-size 14px
        margin 10px

        span {
            display inline-block
            margin-right 10px
        }

        a {
            color #27282cbf
        }
    }

    .getback {
        margin-bottom 20px

        a, a:hover {
            color #3498db
            line-height 20px
        }
    }
}

#footer {
    background #fff
    box-shadow 0px 0px 12px 0px #0000001a
    padding 30px 0
    color #222222
    font-size 14px

    .content {
        width 80%
        max-width 960px
        margin auto

        div {
            margin-top 5px
        }
    }
}
</style>
