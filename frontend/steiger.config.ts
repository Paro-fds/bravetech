import { defineConfig } from 'steiger';
import fsd from '@feature-sliced/steiger-plugin';

// Linter d'architecture Feature-Sliced Design, contrôle attendu par le cours : `npx steiger src`
export default defineConfig([...fsd.configs.recommended]);
