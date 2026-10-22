<template>
  <div class="home">
    <div class="centered-content">
      <Encoder/>
      <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import Encoder from '@/components/Encoder.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld,
    Encoder
  }
}
</script>

<style scoped lang="scss">
.home{
  text-align: center;
  
  display: flex;
  justify-content: center;
  align-items: center;
  
}
.centered-content {
  /* 根据需要调整内部内容的宽度 */
  width: 20%;
}

</style>
