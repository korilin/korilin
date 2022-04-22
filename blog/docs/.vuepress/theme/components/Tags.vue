<template>
    <span style="margin-left: 20px">
        <span
            class="tag"
            v-if="typeof tags == 'string'"
            :style="{ background: randomColor() }"
            >{{ tags }}</span
        >
        <span
            class="tags tag"
            v-else
            v-for="tag in tags"
            :key="tag"
            :style="{ background: randomColor() }"
            >{{ tag }}</span
        >
    </span>
</template>

<script>
const colors = [
    "#f44336",
    "#e91e63",
    "#3f51b5",
    "#2196f3",
    "#03a9f4",
    "#00bcd4",
    "#009688",
    "#4caf50",
    "#ffc107",
    "#ff9800",
    "#607d8b",
];

export default {
    props: ["tags"],
    methods: {
        randomColor() {
            return colors[Math.round(Math.random() * (colors.length - 1))];
        },
    },
};
</script>

<style lang="stylus" scoped>
.tags {
    margin-right: 10px;
}

.tag {
    font-size: 10px;
    padding: 3px 10px;
    border-radius: 50px;
    background: black;
    color: white;
    user-select: none;
}
</style>