<template>
    <div class="container">
        <div class="hero">
            <div class="desc">
                <h1>Welcome to my blog!</h1>
                <h2>Hello! I'm Kori Lin, a Full Stack developer.</h2>
                <div class="icons">
                    <template v-for="platform in $themeConfig.socialPlatform">
                        <a
                            :href="platform.href"
                            v-bind:key="platform.name"
                            target="_blank"
                        >
                            <img
                                :src="$withBase(platform.icon)"
                                :alt="platform.name"
                            />
                        </a>
                    </template>
                </div>
            </div>

            <div class="img">
                <img :src="$withBase($themeConfig.logo)" alt="log" />
            </div>
        </div>
        <div class="kug">
            <h2>KUG</h2>
            <p>
                如果你也在学习 Kotlin，或对 Kotlin 这门语言感兴趣，欢迎你加入到
                Kotlin User Group，你可以在 JetBrains Kotlin 官网中的 Kotlin
                User Groups List 中找到你感兴趣的 User Group。
            </p>
            <div>
                <a
                    target="_blank"
                    href="https://kotlinlang.org/user-groups/user-group-list.html"
                    class="kug-btn"
                    >在 kotlinlang.org 查看 KUG</a
                >
            </div>
        </div>
        <div class="about">
            <h2>About</h2>
            <div>
                <Content class="theme-default-content" />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Home",
};
</script>

<style lang="stylus" scoped>
.container {
    width 100%
    margin-top 60px
    padding 60px 0

    .hero {
        margin auto
        display flex
        flex-direction column-reverse
        justify-content space-around
        align-items center
        width 80%

        @media (min-width 1200px) {
            flex-direction row
            justify-content center
            width 90%
            height 70vh
        }

        .desc {
            padding-top 3rem

            @media (min-width 1200px) {
                width 48%
            }

            display flex
            flex-direction column
            justify-content center

            h1 {
                margin 0 0 10px 0
                font-size 48px
                font-weight 700
                line-height 56px
                color black
            }

            h2 {
                border 0
                margin-bottom 50px
                font-size 24px
                font-weight normal
            }

            .icons {
                padding 0 10px

                a {
                    margin 0 10px
                }

                img {
                    width 40px
                }
            }
        }

        .img {
            img {
                width 100%
                animation move 2.5s linear infinite
                position relative
            }

            @keyframes move {
                0% {
                    top 0
                }

                25% {
                    top -10px
                }

                50% {
                    top 0
                }

                75% {
                    top 10px
                }

                100% {
                    top 0
                }
            }

            @media (min-width 1200px) {
                width 48%

                img {
                    max-width 500px
                }
            }

            @media (max-width 1200px) {
                img {
                    max-width 250px
                }
            }

            text-align center
        }
    }

    .about, .kug {
        padding 2rem 2.5rem
        max-width 960px !important
        margin auto

        li::before {
            content '\eb79'
        }

        h2 {
            text-align center
            border 0
            font-size 32px

            &::after, &::before {
                content ''
                width 50px
                height 2px
                background #3498db
                display inline-block
                margin 10px 15px
            }
        }

        .kug-btn {
            font-weight 600
            font-size 14px
            letter-spacing 1px
            display inline-block
            padding 12px 32px
            border-radius 50px
            transition 0.3s
            line-height 1
            color #3498db
            -webkit-animation-delay 0.8s
            animation-delay 0.8s
            margin-top 6px
            border 2px solid #3498db

            &:hover {
                background #3498db
                color #fff
                text-decoration none
            }
        }
    }
}
</style>