<template>
  <div id="notFound">
    <div class="box">
      <p class="head">404</p>
      <p class="text">Diese Seite existiert nicht (mehr).</p>
      <p class="descr">Die aufgerufene Seite <i>{{ path }}</i> konnte nicht gefunden werden. Dies kann mehrere Gründe haben wie beispielsweise einen Tippfehler, die Seite wurde entfernt oder andere technische Gründe.</p>
      <router-link to="/search">Zurück zur Startseite</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue" ;
import { useRoute } from "vue-router";

const route = useRoute();

const path = ref(route.path);
</script>  