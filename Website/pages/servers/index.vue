<template>
  <div>
    <ServerNames
      v-for="index in names"
      :key="index.id"
      :id="index.id"
      :servername="index.name"
      :uplink="index.uplink"
      :status="index.status"
      :location="index.location"
    />
  </div>
</template>

<script>
import ServerNames from '../../components/ServerNames.vue'
import axios from 'axios'

export default {
  components: {
    ServerNames,
  },
  data() {
    return {
      names: [],
      url: 'https://api.quix.click/api/v1/client/backends',
      Authorization: this.$auth.$storage.getState('_token.local')
    }
    //this.$store.state.token   this.$auth.$storage._state
  },
  async created() {
    console.log('From Server Page:', this.Authorization)
    try {
      const res = await axios.get(this.url, {
        headers: {
          Authorization: `${this.Authorization}`,
        },
      })
      console.log(this.Authorization)
      this.names = res.data.data
      //console.log("BackendPage:",res)
    } catch (error) {
      console.log(error)
    }
  },
}
</script>

<style>
* {
  color: #bbe1fa;
}
</style>