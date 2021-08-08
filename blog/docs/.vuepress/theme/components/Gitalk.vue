<template>
    <div id="gitalk-container"></div>
</template>

<script>
import Gitalk from "gitalk";
export default {
    mounted() {
        var gitalk = new Gitalk({
            clientID: "b7aa589ca8f3de3b34fc",
            clientSecret: "9aed479aabee6e5cf3843b672f33c989deb3d83a",
            repo: "korilin",
            owner: "korilin",
            admin: ["korilin"],
            id: location.pathname, // Ensure uniqueness and length less than 50
            distractionFreeMode: false, // Facebook-like distraction free mode
        });

        gitalk.render("gitalk-container");
    },
};
</script>
