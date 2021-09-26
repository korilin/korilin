<template>
    <main class="page">
        <div class="theme-default-content">
            <div class="getback">
                <router-link to @click="$router.go(-1)">
                    &lt; 返回
                </router-link>
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
            <Gitalk />
        </div>
    </main>
</template>

<script>
import Gitalk from "./Gitalk.vue";

export default {
    components: { Gitalk },
    props: ["sidebarItems"],
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
    padding-bottom: 2rem;
    display: block;

    .head {
        border-top: 1px dashed #27282c33;
        border-bottom: 1px dashed #27282c33;
        padding: 25px 0;
        margin-bottom: 20px;
    }

    .title {
        text-align: center;
    }

    .info {
        text-align: center;
        color: #27282cbf;
        font-size: 15px;
        margin: 10px;

        span {
            display: inline-block;
            margin-right: 10px;
        }

        a {
            color: #27282cbf;
        }
    }

    .getback {
        margin-bottom: 20px;

        a, a:hover {
            color: #3498db;
            line-height: 20px;
        }
    }
}
</style>
