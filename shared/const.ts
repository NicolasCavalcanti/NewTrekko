export const COOKIE_NAME = "app_session_id";
export const ONE_YEAR_MS = 1000 * 60 * 60 * 24 * 365;
export const AXIOS_TIMEOUT_MS = 30_000;
export const UNAUTHED_ERR_MSG = 'Please login (10001)';
export const NOT_ADMIN_ERR_MSG = 'You do not have required permission (10002)';

/**
 * Taxa da plataforma sobre cada reserva paga pela Trekko, em %.
 * É o valor que o guia vê no cadastro, na criação de expedição e no painel financeiro;
 * o servidor usa o mesmo número no checkout, no webhook do Mercado Pago e nos ganhos do guia.
 */
export const PLATFORM_FEE_PERCENT = 4;
