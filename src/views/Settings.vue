<template>
  <div>
    <b-list-group>
      <b-list-group-item id="logout" button @click="logout()">
        Logout
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
export default {
  methods: {
    logout () {
      this.$store.dispatch('logout')
      this.$router.push('/login')
    }
  }
}
</script>

<style>

</style>