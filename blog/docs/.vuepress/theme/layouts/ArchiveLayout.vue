<template>
    <div class="theme-default-content archive">
        <div class="toolbar">
            <h1>近期文章</h1>
            <div class="tag-select">
                分类：
                <a
                    v-bind:class="
                        selected.includes(tag) ? 'select selected' : 'select'
                    "
                    v-for="tag in $themeConfig.allTag"
                    v-bind:key="tag"
                    @click="onSelect(tag)"
                >
                    {{ tag }}
                </a>
            </div>
        </div>
        <div class="posts">
            <transition name="post" v-for="page in pages" :key="page.path">
                <div class="post" v-show="isSelect(page.frontmatter.tags)">
                    <h1 class="title">
                        <router-link :to="page.path">
                            {{ page.title }}
                        </router-link>
                    </h1>
                    <div class="info">
                        <span>{{ getDate(page.frontmatter.date) }}</span>
                        <Tags :tags="page.frontmatter.tags" />
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
            </transition>
        </div>
    </div>
</template>

<script>
import Tags from "../components/Tags.vue";

export default {
    components: { Tags },
    created() {
        this.$site.pages.forEach((page) => {
            if (
                page.path.match("/archive/") &&
                page.path != "/archive/" &&
                page.frontmatter.hidden != true
            ) {
                this.pages.push(page);
            }
        });
    },
    data() {
        return {
            selected: [],
            pages: [],
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
        onSelect(tag) {
            let index = this.selected.indexOf(tag);
            if (index >= 0) {
                this.selected.splice(index, 1);
            } else {
                this.selected.push(tag);
            }
        },
        isSelect(tags) {
            if (this.selected.length == 0) return true;
            if (tags == undefined) return false;
            if (typeof tags == "string") {
                return this.selected.includes(tags);
            }
            for (let index = 0; index < tags.length; index++) {
                const tag = tags[index];
                if (this.selected.includes(tag)) return true;
            }
            return false;
        },
    },
};
</script>

<style scoped lang="stylus">
.archive {
    h1 {
        font-size: 1.7rem;
    }

    h2 {
        font-size: 1.5rem;
    }

    h3 {
        font-size: 1.3rem;
    }
}

.post-enter-active, .post-leave-active {
    transition: all 0.8s ease;
    max-height: 200px;
}

.post-enter, .post-leave-to {
    opacity: 0;
    max-height: 0px;
    padding: 0px;
}

.toolbar {
    // padding-bottom: 10px;
    .tag-select {
        padding: 20px 0;
        // border-top: 1px solid #27282c33;
        border-bottom: 1px solid #27282c33;

        .select {
            font-size: 14px;
            letter-spacing: 1px;
            display: inline-block;
            padding: 5px 10px;
            border-radius: 50px;
            transition: 0.3s;
            line-height: 1;
            border: 1px solid rgba(39, 40, 44, 0.5);
            margin: 5px 5px;
            color: rgba(39, 40, 44, 0.5);
            background: white;
            transition: 0.2s all;
            user-select: none;

            &:hover {
                color: #2196f3;
                border: 1px solid #2196f3;
                text-decoration: none;
            }
        }

        .selected {
            color: white !important;
            background: #2196f3 !important;
            border: 1px solid #2196f3 !important;
        }
    }
}

.posts {
    .post {
        border-bottom: 1px dashed #9699a54d;
        padding: 0 30px;
        overflow: hidden;

        .title {
            margin-top: 20px;

            a {
                color: #2c3e50;
                text-decoration: none;
                font-weight: bold !important;
                transition: all 0.2s;

                &:hover {
                    color: #3498db;
                }

                &:hover {
                }
            }
        }

        .info {
            color: #27282cbf;
            font-size: 14px;
            margin: 10px 0;

            span {
                display: inline-block;
                margin-right: 10px;
            }

            a {
                color: #27282cbf;
            }
        }

        .footer {
            margin-top: 20px;
            margin-bottom: 30px;

            .readmore {
                font-size: 14px;
                border: 1px solid #27282c33;
                padding: 4px 15px;
                border-radius: 10px;
                text-decoration: none;
                color: #27282cb3;
                transition: all 0.2s;

                &:hover {
                    border: 1px solid #3498db;
                    color: #3498db;
                }
            }
        }
    }
}
</style>