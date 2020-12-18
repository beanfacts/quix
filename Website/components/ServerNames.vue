<template>
  <nuxt-link :to="'servers/' + id" class="noline">
    <div class="servernames">
      <h3>
        <strong>{{ servername }}</strong>
      </h3>
      <pre><b>Server Uplink:</b> {{uplink}}      <b>Status:</b> {{status}}      <b>Location:</b> {{location}}</pre>
    </div>
  </nuxt-link>
</template>

<script>
export default {
  name: 'ServerNames',
  props: ['id', 'servername', 'uplink', 'status', 'location'],
}
</script>

<style>
.servernames {
  padding: 1rem;
  border: 1px solid #ccc;
  margin: 1rem 0;
  text-decoration: none;
}
.noline {
  text-decoration: none;
}

* {
  color: #bbe1fa;
}
</style>