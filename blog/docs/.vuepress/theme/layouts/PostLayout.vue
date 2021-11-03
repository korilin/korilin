<template>
    <div class="theme-default-content page">
        <div class="getback">
            <span @click="goBefore()" style="cursor: pointer; color: #3498db">
                &lt; 返回
            </span>
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
</template>

<script>
import Gitalk from "../components/Gitalk.vue";

export default {
    name: "PostLayout",
    components: { Gitalk },
    methods: {
        getDate(date) {
            var d = new Date(date);
            var year = d.getFullYear();
            var month = d.getMonth() + 1;
            var day = d.getDate();
            return year + "年" + month + "月" + day + "日";
        },
        goBefore() {
            this.$router.go(-1);
        },
    },
};
</script>

<style lang="stylus" scoped>
.page {
    padding-bottom: 2rem;
    display: block;

    @media (min-width: 959px) {
        padding-left: 22.5rem !important;
    }

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
