<template>
    <div
        id="global-layout"
        class="theme-container"
        :class="pageClasses"
        @touchstart="onTouchStart"
        @touchend="onTouchEnd"
    >
        <Navbar v-if="shouldShowNavbar" @toggle-sidebar="toggleSidebar" />
        <div class="sidebar-mask" @click="toggleSidebar(false)" />
        <Sidebar :items="sidebarItems" @toggle-sidebar="toggleSidebar" />
        <component :is="layout" />
        <Footer class="f-to-h" />
    </div>
</template>

<script>
import Navbar from "@parent-theme/components/Navbar.vue";
import Sidebar from "@parent-theme/components/Sidebar.vue";
import { resolveSidebarItems } from "@parent-theme/util";

import Footer from "@theme/components/Footer.vue";
import PostLayout from "./PostLayout.vue";

export default {
    components: { Navbar, Footer, PostLayout, Sidebar },
    data() {
        return {
            isSidebarOpen: false,
        };
    },
    computed: {
        shouldShowNavbar() {
            const { themeConfig } = this.$site;
            const { frontmatter } = this.$page;
            if (frontmatter.navbar === false || themeConfig.navbar === false) {
                return false;
            }
            return (
                this.$title ||
                themeConfig.logo ||
                themeConfig.repo ||
                themeConfig.nav ||
                this.$themeLocaleConfig.nav
            );
        },
        shouldShowSidebar() {
            const { frontmatter } = this.$page;
            return (
                !frontmatter.home &&
                frontmatter.sidebar !== false &&
                this.sidebarItems.length
            );
        },
        layout() {
            if (this.$page.path) {
                if (this.$frontmatter.layout) {
                    return this.$frontmatter.layout;
                }
                return "PostLayout";
            }
            return "NotFound";
        },
        sidebarItems() {
            return resolveSidebarItems(
                this.$page,
                this.$page.regularPath,
                this.$site,
                this.$localePath
            );
        },
        pageClasses() {
            const userPageClass = this.$page.frontmatter.pageClass;
            return [
                {
                    "no-navbar": !this.shouldShowNavbar,
                    "sidebar-open": this.isSidebarOpen,
                    "no-sidebar": !this.shouldShowSidebar,
                },
                userPageClass,
            ];
        },
    },
    mounted() {
        this.$router.afterEach(() => {
            this.isSidebarOpen = false;
        });
    },
    methods: {
        toggleSidebar(to) {
            this.isSidebarOpen =
                typeof to === "boolean" ? to : !this.isSidebarOpen;
            this.$emit("toggle-sidebar", this.isSidebarOpen);
        },

        // side swipe
        onTouchStart(e) {
            this.touchStart = {
                x: e.changedTouches[0].clientX,
                y: e.changedTouches[0].clientY,
            };
        },

        onTouchEnd(e) {
            const dx = e.changedTouches[0].clientX - this.touchStart.x;
            const dy = e.changedTouches[0].clientY - this.touchStart.y;
            if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 40) {
                if (dx > 0 && this.touchStart.x <= 80) {
                    this.toggleSidebar(true);
                } else {
                    this.toggleSidebar(false);
                }
            }
        },
    },
};
</script>

<style lang="stylus" scoped>
.f-to-h {
    z-index: 100;
    position: absolute;
    width: 100%;
    bottom: 0px;
}
</style>