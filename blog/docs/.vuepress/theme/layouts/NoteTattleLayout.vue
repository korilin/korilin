<template>
    <div class="theme-default-content note-tattle">
        <div>
            <h1 class="t">笔记 & 杂谈</h1>
        </div>

        <template v-for="page in pages">
            <div class="post" v-bind:key="page.path">
                <div class="info">
                    <span>{{ getDate(page.frontmatter.date) }}</span>
                </div>
                <div class="excerpt">
                    <div class="title">{{ page.title }}</div>

                    <div v-html="page.excerpt"></div>

                    <div class="footer">
                        <router-link :to="page.path" class="readmore">阅读全文</router-link>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<script>
export default {
    created() {
        this.$site.pages.forEach((page) => {
            if (
                page.path.match("/note-tattle/") &&
                page.path != "/note-tattle/" &&
                page.frontmatter.hidden != true
            ) {
                this.pages.push(page);
            }
        });
    },
    data() {
        return {
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
    },
};
</script>

<style scoped lang="stylus">
h1 {
    font-size: 1.7rem !important;
}

.t {
    color: #3498db;
    margin: 0.67em 0 50px;
}

.post {
    margin-bottom: 50px;
    

    .title {
        font-size: 1.7rem;
        font-weight: bold;
        margin-bottom: 20px;
        text-decoration: solid;
        text-align: center;
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

    .excerpt {
        border: dashed 2px #d0d7de;
        border-radius: 6px;
        padding: 30px;
        // background: #f6f8fa;
    }

    .footer {
        margin-top: 30px;
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