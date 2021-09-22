<template>
    <div class="archive">
        <div class="toolbar">
            <h1>近期文章</h1>
            <div class="category-select">
                分类：
                <a
                    v-bind:class="
                        selected.includes(category)
                            ? 'select selected'
                            : 'select'
                    "
                    v-for="category in $themeConfig.categories"
                    v-bind:key="category"
                    @click="onSelect(category)"
                >
                    {{ category }}
                </a>
            </div>
        </div>
        <div class="posts">
            <template v-for="page in this.$site.pages">
                <div
                    class="post"
                    v-if="
                        page.path != '/' &&
                        page.path != '/about/' &&
                        page.path != '/archive/' &&
                        page.path != '/tittle-tattle/' &&
                        selected.includes(page.frontmatter.category) &&
                        page.frontmatter.hidden != true
                    "
                    v-bind:key="page.path"
                >
                    <div class="title">
                        <router-link :to="page.path">
                            <h1>{{ page.title }}</h1>
                        </router-link>
                    </div>
                    <div class="info">
                        <span>{{ getDate(page.frontmatter.date) }}</span>
                        <span style="margin-left: 20px">{{
                            page.frontmatter.category
                        }}</span>
                    </div>
                    <div class="excerpt">
                        <div v-html="page.excerpt"></div>
                    </div>
                    <div class="footer">
                        <router-link :to="page.path" class="readmore">
                            阅读全文
                        </router-link>
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>

<script>
export default {
    name: "Archive",
    created() {
        for (var i = 0; i < this.$themeConfig.categories.length; i++) {
            this.selected.push(this.$themeConfig.categories[i]);
        }
    },
    data() {
        return {
            selected: [],
        };
    },
    methods: {
        getDate(date) {
            var d = new Date(date);
            var year = d.getFullYear();
            var month = d.getMonth() + 1;
            var day = d.getDate();
            return year + "年" + month + "月" + day + "日";
        },
        onSelect(category) {
            let index = this.selected.indexOf(category);
            if (index >= 0) {
                this.selected.splice(index, 1);
            } else {
                this.selected.push(category);
            }
        },
    },
};
</script>

<style scoped lang="stylus">
.toolbar {
    padding-bottom 10px

    .category-select {
        padding 20px 0
        border-top 1px solid #27282c33
        border-bottom 1px solid #27282c33

        .select {
            font-size 14px
            letter-spacing 1px
            display inline-block
            padding 5px 10px
            border-radius 50px
            transition 0.3s
            line-height 1
            border 1px solid rgba(39, 40, 44, 0.5)
            margin 5px 5px
            color rgba(39, 40, 44, 0.5)
            background white
            transition 0.2s all
            user-select none

            &:hover {
                color #3498db
                border 1px solid #3498db
                text-decoration none
            }
        }

        .selected {
            color white !important
            background #57bcff !important
            border 1px solid #57bcff !important
        }
    }
}

.posts {
    .post {
        border-bottom 1px solid #9699a533
        padding 10px 0 30px

        .title {
            a {
                color #2c3e50
                text-decoration none
                font-weight bold !important
                transition all 0.2s

                &:hover {
                    color #3498db
                }

                &:hover {
                }
            }
        }

        .info {
            color #27282cbf
            font-size 14px
            margin 10px 0

            span {
                display inline-block
                margin-right 10px
            }

            a {
                color #27282cbf
            }
        }

        .footer {
            margin-top 20px

            .readmore {
                font-size 14px
                border 1px solid #27282c33
                padding 4px 15px
                border-radius 10px
                text-decoration none
                color #27282cb3
                transition all 0.2s

                &:hover {
                    border 1px solid #3498db
                    color #3498db
                }
            }
        }
    }
}
</style>