<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title class="text-weight-bold">
          <q-icon name="flight_takeoff" size="28px" class="q-mr-sm" />
          TravesIA
        </q-toolbar-title>

        <!-- User Menu -->
        <q-btn flat round dense icon="notifications">
          <q-badge color="red" floating>3</q-badge>
        </q-btn>

        <q-btn-dropdown flat round dense icon="account_circle">
          <q-list>
            <q-item-label header>{{ authStore.fullName }}</q-item-label>
            <q-item clickable v-close-popup @click="onProfile">
              <q-item-section avatar>
                <q-icon name="person" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Perfil</q-item-label>
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="onSettings">
              <q-item-section avatar>
                <q-icon name="settings" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Configuración</q-item-label>
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-close-popup @click="onLogout">
              <q-item-section avatar>
                <q-icon name="logout" color="negative" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Cerrar Sesión</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-scroll-area class="fit">
        <q-list padding>
          <q-item-label header class="text-weight-bold text-grey-8">
            MENÚ PRINCIPAL
          </q-item-label>

          <q-item
            clickable
            v-ripple
            :to="link.to"
            v-for="link in menuLinks"
            :key="link.title"
            :active="route.path === link.to"
            active-class="bg-primary text-white"
          >
            <q-item-section avatar>
              <q-icon :name="link.icon" />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ link.title }}</q-item-label>
              <q-item-label caption v-if="link.caption">{{
                link.caption
              }}</q-item-label>
            </q-item-section>
          </q-item>

          <q-separator class="q-my-md" />

          <q-item-label header class="text-weight-bold text-grey-8">
            GESTIÓN
          </q-item-label>

          <q-item
            clickable
            v-ripple
            :to="link.to"
            v-for="link in managementLinks"
            :key="link.title"
            :active="route.path.startsWith(link.to)"
            active-class="bg-primary text-white"
          >
            <q-item-section avatar>
              <q-icon :name="link.icon" />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ link.title }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'src/stores/auth';

defineOptions({
  name: 'MainLayout',
});

const router = useRouter();
const route = useRoute();
const $q = useQuasar();
const authStore = useAuthStore();

interface MenuLink {
  title: string;
  caption?: string;
  icon: string;
  to: string;
}

const menuLinks: MenuLink[] = [
  {
    title: 'Dashboard',
    icon: 'dashboard',
    to: '/dashboard',
  },
  {
    title: 'Calendario',
    icon: 'event',
    to: '/calendar',
  },
  {
    title: 'Reportes',
    icon: 'assessment',
    to: '/reports',
  },
];

const managementLinks: MenuLink[] = [
  {
    title: 'Circuitos',
    icon: 'map',
    to: '/programs',
  },
  {
    title: 'Grupos',
    icon: 'groups',
    to: '/groups',
  },
  {
    title: 'Pasajeros',
    icon: 'person',
    to: '/passengers',
  },
  {
    title: 'Proveedores',
    icon: 'business',
    to: '/suppliers',
  },
  {
    title: 'Operaciones',
    icon: 'hotel',
    to: '/operations',
  },
  {
    title: 'Finanzas',
    icon: 'attach_money',
    to: '/financial',
  },
  {
    title: 'Documentos',
    icon: 'folder',
    to: '/documents',
  },
];

const leftDrawerOpen = ref(false);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}

function onProfile() {
  router.push('/profile');
}

function onSettings() {
  router.push('/settings');
}

async function onLogout() {
  $q.dialog({
    title: 'Cerrar Sesión',
    message: '¿Estás seguro de que deseas cerrar sesión?',
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    await authStore.logout();
    router.push('/login');
    $q.notify({
      type: 'positive',
      message: 'Sesión cerrada exitosamente',
      position: 'top',
    });
  });
}
</script>
