<template>

    <div class="explore-right">
            <RouterLink  class="link" to="/posts/new">New Post</RouterLink>
        </div>

  <div v-if="loading">Loading...</div>
  <div v-if="error">{{ error }}</div>
  <ul v-if="!loading && !error">
    <div id="user-posts">
      <h6 v-if="posts.length === 0" class="no-posts">This user has no posts</h6>
      <div v-for="post in posts" class="post">
        <div>
        {{post.username}}
        </div>
        <img
          :title="post.caption"
          width="400px"
          height="400px"
          :src="'/uploads/' + post.photo"
          :alt="post.caption"
        />
        <div>
       {{ post.caption }}
        </div>
        <div>
        {{ post.created_on}}
        </div>
      </div>
    </div>
  </ul>

</template>


<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { jwtDecode } from 'jwt-decode';
import moment from 'moment';

const router = useRouter();
const posts = ref([]);
const loading = ref(false);
const error = ref(null);

const fetchPosts = async (token) => {
    loading.value = true;
    error.value = null; // Clear previous errors
    try {
        const response = await fetch('/api/v1/posts', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        });
        if (!response.ok) {
            throw new Error(`Failed to fetch posts: ${response.status}`);
        }
        const jsonData = await response.json(); // Parse JSON
        posts.value = jsonData;
        // console.log('Received posts:', jsonData);
    } catch (err) {
        error.value = err.message;
        console.log('Error fetching posts:', err);
    } finally {
        loading.value = false;
    }
};


onMounted(() => {
    const token = localStorage.getItem('token');
    if (!token) {
        router.push({ name: 'login' });
        return;
    }
    fetchPosts(token);
});

</script>



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