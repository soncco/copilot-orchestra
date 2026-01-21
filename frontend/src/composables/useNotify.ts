/**
 * Composable para notificaciones
 * Wrapper de Quasar Notify para uso consistente en toda la app
 */
import { Notify } from 'quasar';

export type NotifyType = 'positive' | 'negative' | 'warning' | 'info';

export interface NotifyOptions {
  message: string;
  type?: NotifyType;
  position?:
    | 'top'
    | 'bottom'
    | 'left'
    | 'right'
    | 'top-left'
    | 'top-right'
    | 'bottom-left'
    | 'bottom-right'
    | 'center';
  timeout?: number;
  actions?: Array<{
    label: string;
    color?: string;
    handler: () => void;
  }>;
}

export function useNotify() {
  const notify = (options: NotifyOptions) => {
    Notify.create({
      message: options.message,
      type: options.type || 'info',
      position: options.position || 'top',
      timeout: options.timeout || 3000,
      actions: options.actions,
    });
  };

  const success = (message: string, timeout = 3000) => {
    notify({ message, type: 'positive', timeout });
  };

  const error = (message: string, timeout = 5000) => {
    notify({ message, type: 'negative', timeout });
  };

  const warning = (message: string, timeout = 4000) => {
    notify({ message, type: 'warning', timeout });
  };

  const info = (message: string, timeout = 3000) => {
    notify({ message, type: 'info', timeout });
  };

  return {
    notify,
    success,
    error,
    warning,
    info,
  };
}
