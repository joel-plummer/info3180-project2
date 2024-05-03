<template>
    <div class="explore-right">
      <RouterLink class="link" to="/posts/new">New Post</RouterLink>
    </div>
  
    <div v-if="loading">Loading...</div>
    <div v-if="error">{{ error }}</div>
  
    <ul v-if="!loading && !error">
      <div id="user-posts">
        <h6 v-if="posts.length === 0" class="no-posts">This user has no posts</h6>
        <div v-for="post in posts" class="post">
          <div class="post-header">
            <!-- <div class="profile-pic">{{ post.profile_pic }}</div> -->
            <div class="username">{{ post.username }}</div>
          </div>
          <div class="post-content">
            <img
              :title="post.caption"
              width="400px"
              height="400px"
              :src="'/uploads/' + post.photo"
              :alt="post.caption"
            />
            <div class="caption">{{ post.caption }}</div>
            <div class="post-footer"> 
                <!-- <div class="likes">{{ post.likes }}</div> -->
                <div class="date">{{ post.created_on }}</div>
            </div>  
          </div>
        </div>
      </div>
    </ul>
  </template>
  
  <style>
  .explore-right {
    flex: 1;
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
    padding-right: 300px;
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
  #user-posts{
    padding-left: 500px;
    display: grid;
    grid-template-columns: 600px;
  }
  .post {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 40px;
  overflow: hidden;
}
  
  .post-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .username {
    font-weight: bold;
    padding-top: 5px;
    padding-left: 5px;
  }
  .date {
    color: #888;
  }
  
  .post-content {
    display: flex;
    flex-direction: column;
  }
  
  .post-content img {
    width: 595px;
    height: 500px;
    margin-bottom: 10px;
  }
  
  .caption {
    margin-top: 10px;
  }
  </style>
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



