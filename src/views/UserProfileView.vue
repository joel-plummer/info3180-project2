<script setup>
import { ref, onMounted } from "vue";
import { jwtDecode } from "jwt-decode";
import { useRouter } from "vue-router";

const router = useRouter();
const posts = ref([]);
const followers = ref([]);
const userInfo = ref({});

onMounted(async () => {
  const token = localStorage.getItem("token");

  if (!token) {
    router.push({ name: "login" });
    return; 
  }

  try {
    const decodedToken = jwtDecode(token);
    userInfo.value = decodedToken;

    const getUserPosts = async () => {
      const data = await fetch(`/api/v1/users/${decodedToken.sub}/posts`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      posts.value = await data.json();
    };

    const getFollowers = async () => {
      const data = await fetch(`/api/v1/users/${userInfo.sub}/followers`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      followers.value = await data.json();
    };

    getUserPosts();
    getFollowers();
  } catch (error) {
    console.error("Error fetching user data:", error);
    router.push({ name: "login" });
  }
});

const setDefaultImage = (event) => {
  event.target.src = "/uploads/default-image.jpg"; 
};
</script>


<template>
  <div class="profile-container">
    <div class="user-details-container">
      <div id="profile-photo">
        <img
          :src="'/uploads/' + userInfo.profile_photo"
          :alt="'photo of ' + userInfo.firstname + ' ' + userInfo.lastname"
          @error="setDefaultImage"
        />
      </div>

      <div id="user-info">
        <h2 class="name-text">
          {{ userInfo.firstname }} {{ userInfo.lastname }}
        </h2>

        <p class="location-text">{{ userInfo.location }}</p>
        <small>Member since {{ userInfo.joined_on }}</small>

        <p class="bio">{{ userInfo.biography }}</p>
      </div>

      <div id="acc-info">
        <div id="posts">
          <p class="num" id="posts_num">{{ posts.length }}</p>
          <p class="post-text">Posts</p>
        </div>

        <div id="followers">
          <p class="num" id="followers_num">{{ followers.length }}</p>
          <p class="follower-text">Followers</p>
        </div>
      </div>
    </div>

    <div id="user-posts">
      <h6 v-if="posts.length === 0" class="no-posts">This user has no posts</h6>
      <div v-for="post in posts" class="post">
        <img
          :title="post.caption"
          width="400px"
          height="400px"
          :src="'/uploads/' + post.photo"
          :alt="post.caption"
        />
      </div>
    </div>
  </div>
</template>

<style>
.bio {
  margin-top: 10px;
}

.profile-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.user-details-container {
  display: flex;
  flex-direction: row;
  gap: 50px;
  justify-content: flex-start;
  align-items: center;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 20px;
  width: 60%;
}

#profile-photo img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

#user-info {
  width: 200%;
}

#user-info h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

#user-info p {
  margin-bottom: 5px;
}

#acc-info {
  display: flex;
  gap: 20px;
  width: 100%;
  margin-top: 20px;
}

#posts,
#followers {
  text-align: center;
}

#posts_num,
#followers_num {
  font-size: 38px;
  font-weight: bold;
}

#user-posts {
  margin-top: 20px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
.no-posts {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100%;
  color: grey;
}

.post {
  margin-bottom: 20px;
}

.post p {
  margin-bottom: 10px;
}

.post img {
  width: 500px;

  height: 400px;
  margin-top: 10px;
}

.follower-text,
.post-text {
  color: grey;
  font-size: 18px;
  font-weight: bolder;
}

.bio,
.location-text {
  margin-top: 10px;
}

small {
  color: lightslategray;
}
</style>
