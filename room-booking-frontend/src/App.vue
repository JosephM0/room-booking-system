<!-- <script setup lang="ts">
import RoomCalendar from './components/RoomCalendar.vue';

</script> -->

<template>
  <div>
    <login v-if="!isLoggedIn" @login-success="loadUser" />
    <div v-else>
      <div class="d-flex justify-content-end mb-3">
        <button class="btn btn-outline-danger btn-sm" @click="logout">
          Logout
        </button>
      </div>

      <RoomCalendar :userGroups="userGroups" />
    </div>
  </div>
</template>

<script>
import Login from './components/Login.vue';
import RoomCalendar from './components/RoomCalendar.vue';
import { fetchCurrentUser } from './services/user';
import { getAccessToken } from './services/auth';

export default {
  data() {
    return {
      userGroups: [],
      isLoggedIn: false,
    };
  },
  components: { Login, RoomCalendar },

  async created() {
    await this.loadUser()
  },

  methods: {
    async loadUser() {
      const user = await fetchCurrentUser();

      if (!user) {
        this.isLoggedIn = false;
        return
      }

      this.userGroups = user.groups || [];
      this.isLoggedIn = true;
    },

    logout() {
      localStorage.removeItem("access_token")
      localStorage.removeItem("refresh_token")

      this.isLoggedIn = false;
      this.userGroups = []
    }
  }
};

</script>