<template>
  <v-app dark>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      app
      class="light-blue darken-4"
    >
      <v-list color="#0f4c75">
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
          color="#3282b8"
          class="pa-2 outlined"
        >
          <!-- light-blue darken-3 -->
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar :clipped-left="clipped" fixed app class="grey darken-4">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <div v-if="$auth.loggedIn">
        <v-btn class="pa2" color="#0f4c75" @click="logout">Logout</v-btn>
      </div>
      <div v-else>
        <v-btn class="pa2 regis" color="#0f4c75" to="/registration"
          >Register</v-btn
        >
        <v-btn class="pa2" color="#0f4c75" to="/login">Login</v-btn>
      </div>
    </v-app-bar>

    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
    <v-footer :absolute="!fixed" app class="grey darken-4">
      <span
        >&copy; {{ new Date().getFullYear() + '   Quix Startup Project' }}</span
      >
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-home',
          title: 'Home',
          to: '/',
        },
        {
          icon: 'mdi-view-dashboard-variant',
          title: 'Dashboard',
          to: '/servers',
        },
        {
          icon: 'mdi-cash',
          title: 'Pricing',
          to: '/pricing',
        },
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Quix The One click Solution',
    }
  },
  head() {
    return {
      title: 'Quix',
    }
  },
  methods: {
    async logout() {
      await this.$auth.logout()
      this.$router.push('/')
      //this.removeToken()
      this.$forceUpdate()
    },
    // async removeToken() {
    //   this.$store.commit('setToken', null)
    //   console.log("User Token Removed")
    // },
  },
}
</script>

<style>
* {
  color: #bbe1fa;
}
.regis {
  margin-left: 1rem;
  margin-right: 1rem;
}
</style>