<template>
    <div class="theme-default-content note-tattle">
        <h1 class="t">笔记 & 杂谈</h1>

        <template v-for="page in this.$site.pages">
            <div
                class="post"
                v-if="
                    page.path.match('/note-tattle/') &&
                    page.path != '/note-tattle/' &&
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
</template>

<script>
export default {
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

<style scoped lang="stylus">
h1 {
    font-size: 1.7rem;
}

h2 {
    font-size: 1.5rem;
}

h3 {
    font-size: 1.3rem;
}

.t {
    margin: 30px !important;
    color: #3498db;
}

.post {
    border: solid 1px #d0d7de;
    border-radius: 6px;
    padding: 30px 50px 50px;
    background: #f6f8fa;

    .title {
        a {
            color: #2c3e50;
            text-decoration: none;
            font-weight: bold !important;
            transition: all 0.2s;

            &:hover {
                color: #3498db;
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
        margin-top: 40px;
        text-align: center;

        .readmore {
            width: 80%;
            display: inline-block;
            font-size: 15px;
            border: 1px solid #27282c33;
            padding: 6px 15px;
            border-radius: 10px;
            text-decoration: none;
            color: #27282cb3;
            transition: all 0.2s;
            background: white;

            &:hover {
                border: 1px solid #3498db;
                color: #3498db;
            }
        }
    }
}
</style>