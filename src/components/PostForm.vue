<template>
    <div class="form-container">
    <div class="post">
    <h1>Add a Post</h1>
    <form @submit.prevent="savePost" id="postForm">
        <div v-if="result.errors">
            <ul class="alert alert-danger">
                <li v-for="error in result.errors">{{ error }}</li>
            </ul>
        </div>
        <div v-if="result.message">
            <div class="alert alert-success">{{ result.message }}</div>
        </div>
        <div class="form-group">
            <label for="caption" class="form-label">Caption</label>
            <textarea row="10" name="caption" class="form-control"></textarea>
        </div>
        <div class="form-group">
            <label for="photo" class="form-label">Upload your photo</label>
            <input type="file" name="photo" class="form-control-file">
        </div>
        <input type="submit" value="Post!">
    </form>
</div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import {jwtDecode} from 'jwt-decode';
import { useRouter } from 'vue-router';

const router = useRouter();
let csrf_token = ref("");
let result = ref([]);
const userId = ref(null);

const getCsrfToken = async () => {
    try {
        const response = await fetch('/api/v1/csrf-token');
        const data = await response.json();
        csrf_token.value = data.csrf_token;
    } catch (error) {
        console.error('Failed to fetch CSRF token', error);
    }
}

onMounted(async () => {
    await getCsrfToken();
    const token = localStorage.getItem("token");
    if (!token) {
        router.push({ name: "login" });
        return; // Prevent further execution
    }
    try {
        let decodedToken = jwtDecode(token);
        userId.value = decodedToken.sub;
    } catch (error) {
        console.error('Failed to decode token', error);
        router.push({ name: "login" });
    }
});

const savePost = async () => {
    let postForm = document.getElementById("postForm");
    let form_data = new FormData(postForm);
    const token = localStorage.getItem("token"); // Ensure token is retrieved here for current scope

    try {
        const response = await fetch(`/api/v1/users/${userId.value}/posts`, {
            method: "POST",
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value,
                'Authorization': "Bearer " + token
            }
        });
        result.value = await response.json();
    } catch (error) {
        console.error('Failed to save post', error);
        result.value = error;
    }
}
</script>


<style>

.form-container{
    align-items: center;
}

.post {
    padding: 20px;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
    border-radius: 10px;
    justify-content: center;
    width: 600px;
    background: rgba(13, 133, 173, 0.2);
    margin: 20px auto;
}
  
  form {
    display: flex;
    flex-direction: column;
    max-width: 500px; 
    justify-content: center;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    margin: 20px 0; 
  }
  
  .form-group > label {
    font-weight: bold;
    margin-bottom: 5px; 
  }
  
  textarea {
    width: 50%; 
    height: 150px; 
    resize: vertical; 
  }
  
  input[type="file"] {
    margin-top: 5px; 
  }
  
  input[type="submit"] {
    margin-top: 20px;
    width: 100px;
    border: none;
    background: rgb(76, 120, 240);
    border-radius: 5%;
    color: #fff;
    align-self: flex-start; 
    height: 40px;
  }
  
  input[type="submit"]:hover {
    cursor: pointer;
    background: rgb(6, 24, 104);
  }
  
  .alert {
    padding-left: 50px;
  }
</style>