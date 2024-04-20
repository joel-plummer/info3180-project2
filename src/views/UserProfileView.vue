<script setup>
import { ref, onMounted } from "vue";


let csrf_token = ref("");
let user = ref([]);
let posts = ref([]);
let followers = ref([]);

let token = localStorage.getItem("token");


let id = localStorage.getItem("user_id");

const getCsrfToken = () => {
  fetch("/api/v1/csrf-token")
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      csrf_token.value = data.csrf_token;
      console.log(csrf_token.value);
    });
};

const fetchUser = async (id) => {
  const res = await fetch(`/api/v1/users/${id}`, {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token,
    },
  });
  const data = await res.json();
  console.log("hii" + token);
  return data;
};

const getFollowers = async (id) => {
  ///api/users/<userId>/follow
  const user = await fetchUser(id);
  id = user.id;
  const res = await fetch(`/api/users/${id}/follow`, {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token,
    },
  });
  const data = await res.json();
  return data;
};

const followUser = async (id) => {
  const targetUserId = id;
  const currentUser = await fetchUser("currentuser");
  // console.log(targetUserId, currentUser.id)
  const res = await fetch(`/api/users/${currentUser.id}/follow`, {
    method: "POST",
    body: JSON.stringify({ follow_id: targetUserId }),
    headers: {
      "X-CSRFToken": csrf_token.value,
      Authorization: "Bearer " + token,
      "Content-Type": "application/json",
    },
  });
  const data = await res.json();

  text.value = "following";

  console.log(data);
};

const fetchPosts = async (id) => {
  const user = await fetchUser(id);
  id = user.id;
  const res = await fetch(`/api/v1/users/${id}/posts`, {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token,
    },
  });
  const data = await res.json();
  return data;
};

onMounted(async () => {
  fetchUser(id).then((data) => {
    user.value = data;
    console.log(data);
  });
  const postData = await fetchPosts(id);
  posts.value = postData;

  const followerData = await getFollowers(id);
  followers.value = followerData;

  getCsrfToken();
});
</script>

<template>
  <div class="profile-container">
    <div class="user-details-container">
      <div id="profile-photo">
        <img
          :src="user.profile_photo"
          :alt="'photo of ' + user.firstname + ' ' + user.lastname"
        />
      </div>

      <div id="user-info">
        <h2>{{ user.firstname }} {{ user.lastname }}</h2>
        <p>{{ user.location }}</p>
        <p>Member since {{ user.joined_on }}</p>
        <p>{{ user.biography }}</p>
      </div>

      <div id="acc-info">
        <div id="posts">
          <p class="num" id="posts_num">{{ posts.length }}</p>
          <p>Posts</p>
        </div>

        <div id="followers">
          <p class="num" id="followers_num">{{ followers.length }}</p>
          <p>Followers</p>
        </div>
      </div>
    </div>

    <div id="user-posts">
      <div v-for="post in posts" class="post">
        <p>The Caption : {{ post.caption }}</p>
        The Image : <img :src="post.photo" :alt="post.caption" />
      </div>
    </div>
  </div>
</template>

<style>
.profile-container {
  max-width: 800px;
  margin: auto;
  border: 1px solid #e1e1e1;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-family: "Arial", sans-serif;
}

.user-details-container {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid #e1e1e1;
}

#profile-photo img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 3px solid #e1e1e1;
  margin-bottom: 10px;
}

#user-info h2 {
  margin: 5px 0;
  color: black;
  font-weight: bold;
}

#user-info p {
  color: #373737;
  font-size: 14px;
  margin: 3px 0;
}

#acc-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

#values {
  display: flex;
  justify-content: center;
  margin-bottom: 15px;
}

#values > div {
  text-align: center;
  margin: 0 10px;
}

#values .num {
  font-size: 1.5em;
  color: #333;
  font-weight: bold;
}

#values p {
  font-size: 0.9em;
  color: #777;
  margin: 0;
}

#user-posts {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 20px;
}

.post {
  width: 48%;
  margin: 1%;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.post img {
  width: 100%;
  height: auto;
  display: block;
}
</style>