/**
 * Logger utility for GPToggle v2.0
 * Simple logging interface for consistent logging across the application
 */

export class Logger {
  private context?: string;

  constructor(context?: string) {
    this.context = context;
  }

  private formatMessage(level: string, message: string): string {
    const timestamp = new Date().toISOString();
    const contextStr = this.context ? `[${this.context}] ` : '';
    return `${timestamp} ${level.toUpperCase()} ${contextStr}${message}`;
  }

  debug(message: string): void {
    if (process.env.NODE_ENV === 'development' || process.env.DEBUG) {
      console.debug(this.formatMessage('debug', message));
    }
  }

  info(message: string): void {
    console.info(this.formatMessage('info', message));
  }

  warn(message: string): void {
    console.warn(this.formatMessage('warn', message));
  }

  error(message: string): void {
    console.error(this.formatMessage('error', message));
  }
}