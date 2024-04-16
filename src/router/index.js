import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserProfileView from '../views/UserProfileView.vue'

const token = localStorage.getItem("token")
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterFormView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginFormView.vue')
    },
    {
      path: '/posts/new',
      name: 'new-post',
      component: () => import('../views/NewPostView.vue')
    },
    {
      path: '/users/:id',
      name: "profile-view",
      component: UserProfileView,
      meta: {auth: true}
    }

  ]
})

// router.beforeEach((to, from, next) => {
//   if (to.meta.auth && !token) {
//     next("/login")
//   } else if (!to.meta.auth && token) {
//     next("/explore")
//   } else {
//     next()
//   }
// })

export default router
