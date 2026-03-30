import{c as d,t as c,g as y}from"./index-B0HQVBH5.js";import{r as l}from"./react-vendor-DViTTRkQ.js";/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const k=d("CircleCheckBig",[["path",{d:"M21.801 10A10 10 0 1 1 17 3.335",key:"yps3ct"}],["path",{d:"m9 11 3 3L22 4",key:"1pflzl"}]]);/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const I=d("LoaderCircle",[["path",{d:"M21 12a9 9 0 1 1-6.219-8.56",key:"13zald"}]]);/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const N=d("MapPin",[["path",{d:"M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0",key:"1r0f0z"}],["circle",{cx:"12",cy:"10",r:"3",key:"ilqhr7"}]]),m="trekko_demo_users",a="trekko_demo_session";function g(e){return{...e,role:"user",photoUrl:null,bio:null,cadasturNumber:e.cadasturNumber??null,cadasturValidated:0,openId:null,loginMethod:"password",passwordHash:null,createdAt:null,updatedAt:null,lastSignedIn:null}}function p(){try{return JSON.parse(localStorage.getItem(m)??"[]")}catch{return[]}}function M(e,s){const t=p().find(r=>r.email.toLowerCase()===e.toLowerCase()&&r.password===s);if(!t)return{error:"E-mail ou senha incorretos"};const o=g(t);return localStorage.setItem(a,JSON.stringify(o)),{user:o}}function O(e){const s=p();if(s.some(r=>r.email.toLowerCase()===e.email.toLowerCase()))return{error:"Este e-mail já está cadastrado"};const t={id:Date.now(),name:e.name,email:e.email,password:e.password,userType:e.userType,cadasturNumber:e.cadasturNumber??null};localStorage.setItem(m,JSON.stringify([...s,t]));const o=g(t);return localStorage.setItem(a,JSON.stringify(o)),{user:o}}function S(){try{const e=localStorage.getItem(a);return e?JSON.parse(e):null}catch{return null}}function w(){localStorage.removeItem(a)}function U(e){const{redirectOnUnauthenticated:s=!1,redirectPath:t=y()}={},o=c.useUtils(),r=c.auth.me.useQuery(void 0,{retry:!1,refetchOnWindowFocus:!1,enabled:!1}),i=c.auth.logout.useMutation({onSuccess:()=>{o.auth.me.setData(void 0,null)}}),h=l.useCallback(async()=>{{w(),window.location.href="/";return}},[i,o]),f=S(),n=l.useMemo(()=>{const u=f;return typeof localStorage<"u"&&localStorage.setItem("manus-runtime-user-info",JSON.stringify(u)),{user:u,loading:!1,error:null,isAuthenticated:!!u}},[f,r.data,r.error,r.isLoading,i.error,i.isPending]);return l.useEffect(()=>{s&&(n.loading||n.user||typeof window>"u"||window.location.pathname!==t&&(window.location.href=t))},[s,t,n.loading,n.user]),{...n,refresh:()=>r.refetch(),logout:h}}export{k as C,I as L,N as M,M as a,O as s,U as u};
