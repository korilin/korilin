<template>
    <main class="page">
        <Navbar />
        <component :is="getLayout(this.$page)" />
        <Footer />
    </main>
</template>

<script setup>
// parent theme
import Navbar from "@vuepress/theme-default/lib/client/components/Navbar.vue";

// local theme
import Footer from "../components/Footer.vue";
import HomeLayout from "./HomeLayout.vue"

import { ref, unref, computed } from "vue";

function getLayout(page) {
    if (page.path) {
        if (page.frontmatter.pageLayout) {
            // 像 v1 的 globalLayout 一样首先检测 layout 是否存在
            return page.frontmatter.pageLayout;
        }
        return "Layout";
    }
    return "NotFound";
}
</script>

<style lang="sass" scoped>
.page
    padding-bottom: 2rem
    padding-left: 0
    display: block

.head
    border-top: 1px solid #27282c33
    border-bottom: 1px solid #27282c33
    padding: 30px 0
    margin-bottom: 20px

    .title
        text-align: center

    .info
        text-align: center
        color: #27282cbf
        font-size: 14px
        margin: 10px

    span
        display: inline-block
        margin-right: 10px

        a
            color: #27282cbf

    .getback
        margin-bottom: 20px

    a, a:hover
        color: #3498db
        line-height: 20px
</style>