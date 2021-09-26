<template>
    <div id="global-layout">
        <Navbar />
        <component :is="layout" />
        <Footer />
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
};
</script>