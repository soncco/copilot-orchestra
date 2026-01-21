import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  // Public routes
  {
    path: '/login',
    component: () => import('pages/LoginPage.vue'),
  },

  // Protected routes
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard',
      },
      {
        path: 'dashboard',
        component: () => import('pages/DashboardPage.vue'),
      },
      {
        path: 'programs',
        component: () => import('pages/IndexPage.vue'), // TODO: Create ProgramsPage
      },
      {
        path: 'groups',
        component: () => import('pages/IndexPage.vue'), // TODO: Create GroupsPage
      },
      {
        path: 'passengers',
        component: () => import('pages/IndexPage.vue'), // TODO: Create PassengersPage
      },
      {
        path: 'suppliers',
        component: () => import('pages/IndexPage.vue'), // TODO: Create SuppliersPage
      },
      {
        path: 'operations',
        component: () => import('pages/IndexPage.vue'), // TODO: Create OperationsPage
      },
      {
        path: 'financial',
        component: () => import('pages/IndexPage.vue'), // TODO: Create FinancialPage
      },
      {
        path: 'documents',
        component: () => import('pages/IndexPage.vue'), // TODO: Create DocumentsPage
      },
      {
        path: 'calendar',
        component: () => import('pages/IndexPage.vue'), // TODO: Create CalendarPage
      },
      {
        path: 'reports',
        component: () => import('pages/IndexPage.vue'), // TODO: Create ReportsPage
      },
      {
        path: 'profile',
        component: () => import('pages/IndexPage.vue'), // TODO: Create ProfilePage
      },
      {
        path: 'settings',
        component: () => import('pages/IndexPage.vue'), // TODO: Create SettingsPage
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
