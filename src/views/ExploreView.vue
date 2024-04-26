<template>

    <div class="explore-right">
            <RouterLink  class="link" to="/posts/new">New Post</RouterLink>
        </div>
</template>


<style>

.explore-right {
    flex: 1;
    display: flex;
    justify-content: center;
 }

 .explore-right .link {
    text-decoration: none;
    color: #fff;
    background: rgb(36, 154, 184);
    height: 30px;
    width: 150px;
    text-align: center;
    border-radius: 3px;
    align-items: center;
 }
</style>