<template>
    <div id="global-layout">
        <Navbar />
        <component :is="layout" />
        <Footer class="f-to-h" />
    </div>
</template>

<script>
import Navbar from "@parent-theme/components/Navbar.vue";
import Footer from "@theme/components/Footer.vue";

export default {
    components: { Navbar, Footer },
    computed: {
        layout() {
            if (this.$page.path) {
                if (this.$frontmatter.layout) {
                    return this.$frontmatter.layout;
                }
                return "Layout";
            }
            return "NotFound";
        },
    },
    created() {
    }
};
</script>

<style lang="stylus" scoped>
.f-to-h {
    margin-top: 60px;
}
</style>