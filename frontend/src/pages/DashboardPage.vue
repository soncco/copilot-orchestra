<template>
  <q-page class="q-pa-md">
    <div class="q-mb-md">
      <div class="text-h4 text-weight-bold">Dashboard</div>
      <div class="text-subtitle2 text-grey-7">
        Bienvenido, {{ authStore.fullName }}
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row q-col-gutter-md q-mb-md">
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="stat-card">
          <q-card-section>
            <div class="row items-center">
              <q-icon name="groups" size="48px" color="primary" />
              <div class="col q-ml-md">
                <div class="text-h6">{{ stats.totalGroups }}</div>
                <div class="text-caption text-grey-7">Grupos Activos</div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="stat-card">
          <q-card-section>
            <div class="row items-center">
              <q-icon name="person" size="48px" color="secondary" />
              <div class="col q-ml-md">
                <div class="text-h6">{{ stats.totalPassengers }}</div>
                <div class="text-caption text-grey-7">Pasajeros</div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="stat-card">
          <q-card-section>
            <div class="row items-center">
              <q-icon name="hotel" size="48px" color="positive" />
              <div class="col q-ml-md">
                <div class="text-h6">{{ stats.totalBookings }}</div>
                <div class="text-caption text-grey-7">Reservas</div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="stat-card">
          <q-card-section>
            <div class="row items-center">
              <q-icon name="attach_money" size="48px" color="warning" />
              <div class="col q-ml-md">
                <div class="text-h6">
                  ${{ stats.totalRevenue.toLocaleString() }}
                </div>
                <div class="text-caption text-grey-7">Ingresos</div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Recent Activities -->
    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-8">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">Grupos Recientes</div>
            <q-list separator>
              <q-item v-for="group in recentGroups" :key="group.id" clickable>
                <q-item-section avatar>
                  <q-avatar color="primary" text-color="white">
                    <q-icon name="groups" />
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ group.code }}</q-item-label>
                  <q-item-label caption>{{ group.program_name }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-chip
                    :color="getStatusColor(group.status)"
                    text-color="white"
                    size="sm"
                  >
                    {{ group.status }}
                  </q-chip>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">Accesos Rápidos</div>
            <div class="q-gutter-sm">
              <q-btn
                unelevated
                color="primary"
                icon="add"
                label="Nuevo Grupo"
                class="full-width"
                @click="onNewGroup"
              />
              <q-btn
                unelevated
                color="secondary"
                icon="person_add"
                label="Nuevo Pasajero"
                class="full-width"
                @click="onNewPassenger"
              />
              <q-btn
                unelevated
                color="positive"
                icon="receipt"
                label="Nueva Factura"
                class="full-width"
                @click="onNewInvoice"
              />
              <q-btn
                unelevated
                color="info"
                icon="upload_file"
                label="Subir Documento"
                class="full-width"
                @click="onUploadDocument"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'src/stores/auth';

const router = useRouter();
const $q = useQuasar();
const authStore = useAuthStore();

// Stats
const stats = ref({
  totalGroups: 0,
  totalPassengers: 0,
  totalBookings: 0,
  totalRevenue: 0,
});

// Recent groups (mock data for now)
const recentGroups = ref([
  {
    id: '1',
    code: 'GRP-2026-001',
    program_name: 'Cusco Mágico',
    status: 'confirmed',
  },
  {
    id: '2',
    code: 'GRP-2026-002',
    program_name: 'Lima Colonial',
    status: 'planning',
  },
  {
    id: '3',
    code: 'GRP-2026-003',
    program_name: 'Machu Picchu Express',
    status: 'in_progress',
  },
]);

onMounted(async () => {
  // TODO: Fetch real stats from API
  stats.value = {
    totalGroups: 24,
    totalPassengers: 156,
    totalBookings: 48,
    totalRevenue: 125000,
  };
});

function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    planning: 'grey',
    confirmed: 'primary',
    in_progress: 'warning',
    completed: 'positive',
    cancelled: 'negative',
  };
  return colors[status] || 'grey';
}

function onNewGroup() {
  router.push('/groups/new');
}

function onNewPassenger() {
  router.push('/passengers/new');
}

function onNewInvoice() {
  router.push('/invoices/new');
}

function onUploadDocument() {
  $q.notify({
    type: 'info',
    message: 'Funcionalidad en desarrollo',
    position: 'top',
  });
}
</script>

<style scoped lang="scss">
.stat-card {
  border-radius: 12px;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-4px);
  }
}
</style>
