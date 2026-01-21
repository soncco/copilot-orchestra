<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="flex flex-center bg-gradient">
        <q-card class="login-card q-pa-md shadow-10">
          <q-card-section class="text-center q-pb-none">
            <div class="text-h4 text-weight-bold text-primary q-mb-sm">
              TravesIA
            </div>
            <div class="text-subtitle2 text-grey-7">
              Sistema de Gestión Turística
            </div>
          </q-card-section>

          <q-card-section>
            <q-form @submit="onSubmit" class="q-gutter-md">
              <q-input
                v-model="username"
                type="text"
                label="Usuario"
                outlined
                :rules="[
                  (val) => !!val || 'El usuario es requerido',
                  (val) => val.length >= 3 || 'Mínimo 3 caracteres',
                ]"
                lazy-rules
                autofocus
              >
                <template v-slot:prepend>
                  <q-icon name="person" />
                </template>
              </q-input>

              <q-input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                label="Contraseña"
                outlined
                :rules="[(val) => !!val || 'La contraseña es requerida']"
                lazy-rules
              >
                <template v-slot:prepend>
                  <q-icon name="lock" />
                </template>
                <template v-slot:append>
                  <q-icon
                    :name="showPassword ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="showPassword = !showPassword"
                  />
                </template>
              </q-input>

              <q-input
                v-if="requiresMFA"
                v-model="mfaCode"
                label="Código MFA (6 dígitos)"
                outlined
                mask="### ###"
                :rules="[
                  (val) => !!val || 'El código MFA es requerido',
                  (val) =>
                    val.replace(/\s/g, '').length === 6 ||
                    'Debe tener 6 dígitos',
                ]"
                lazy-rules
              >
                <template v-slot:prepend>
                  <q-icon name="security" />
                </template>
              </q-input>

              <div class="row justify-between items-center">
                <q-checkbox v-model="rememberMe" label="Recordarme" dense />
                <q-btn
                  flat
                  dense
                  no-caps
                  label="¿Olvidaste tu contraseña?"
                  color="primary"
                  size="sm"
                  @click="onForgotPassword"
                />
              </div>

              <q-btn
                type="submit"
                label="Iniciar Sesión"
                color="primary"
                class="full-width"
                size="lg"
                :loading="loading"
                :disable="loading"
              />

              <div class="text-center q-mt-md">
                <span class="text-grey-7">¿No tienes cuenta?</span>
                <q-btn
                  flat
                  dense
                  no-caps
                  label="Registrarse"
                  color="primary"
                  @click="onRegister"
                />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { useNotify } from 'src/composables/useNotify';

const router = useRouter();
const authStore = useAuthStore();
const { success, error: notifyError, info } = useNotify();

// Form data
const username = ref('');
const password = ref('');
const mfaCode = ref('');
const showPassword = ref(false);
const rememberMe = ref(false);
const requiresMFA = ref(false);
const loading = ref(false);

async function onSubmit() {
  loading.value = true;

  try {
    const credentials = {
      username: username.value,
      password: password.value,
      ...(requiresMFA.value && { mfa_code: mfaCode.value.replace(/\s/g, '') }),
    };

    const response = await authStore.login(credentials);

    if (response.requires_mfa) {
      requiresMFA.value = true;
      info('Ingresa tu código MFA');
      return;
    }

    success('Inicio de sesión exitoso');

    // Redirect to dashboard after a small delay to ensure tokens are saved
    await new Promise((resolve) => setTimeout(resolve, 100));
    router.push('/dashboard');
  } catch (error) {
    notifyError('Credenciales incorrectas');
  } finally {
    loading.value = false;
  }
}

function onForgotPassword() {
  info('Funcionalidad en desarrollo');
}

function onRegister() {
  router.push('/register');
}
</script>

<style scoped lang="scss">
.bg-gradient {
  background: linear-gradient(135deg, #0891b2 0%, #0e7490 50%, #10b981 100%);
}

.login-card {
  width: 100%;
  max-width: 450px;
  border-radius: 16px;
}
</style>
