#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

console.log('\n╔════════════════════════════════════════════════╗');
console.log('║   智能硬件位置追踪系统 - 前端测试              ║');
console.log('╚════════════════════════════════════════════════╝\n');

const tests = [];

// 测试 1: 检查依赖
console.log('测试 1: 检查依赖');
console.log('═'.repeat(50));
try {
  const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf-8'));
  const deps = pkg.dependencies;
  const devDeps = pkg.devDependencies;

  const requiredDeps = ['vue', 'pinia', 'leaflet', 'axios'];
  const requiredDevDeps = ['vite', '@vitejs/plugin-vue'];

  let allOk = true;

  requiredDeps.forEach(dep => {
    if (deps[dep]) {
      console.log(`[OK] ${dep} ${deps[dep]}`);
    } else {
      console.log(`[FAIL] ${dep} 未安装`);
      allOk = false;
    }
  });

  requiredDevDeps.forEach(dep => {
    if (devDeps[dep]) {
      console.log(`[OK] ${dep} ${devDeps[dep]}`);
    } else {
      console.log(`[FAIL] ${dep} 未安装`);
      allOk = false;
    }
  });

  tests.push({ name: '检查依赖', passed: allOk });
} catch (e) {
  console.log(`[FAIL] 错误: ${e.message}`);
  tests.push({ name: '检查依赖', passed: false });
}

// 测试 2: 检查文件结构
console.log('\n测试 2: 检查文件结构');
console.log('═'.repeat(50));
try {
  const requiredFiles = [
    'src/main.js',
    'src/App.vue',
    'src/components/MapView.vue',
    'src/components/DevicePanel.vue',
    'src/services/websocket.js',
    'src/stores/deviceStore.js',
    'index.html',
    'vite.config.js'
  ];

  let allOk = true;
  requiredFiles.forEach(file => {
    const filePath = path.join(__dirname, file);
    if (fs.existsSync(filePath)) {
      console.log(`[OK] ${file}`);
    } else {
      console.log(`[FAIL] ${file} 不存在`);
      allOk = false;
    }
  });

  tests.push({ name: '检查文件结构', passed: allOk });
} catch (e) {
  console.log(`[FAIL] 错误: ${e.message}`);
  tests.push({ name: '检查文件结构', passed: false });
}

// 测试 3: 检查Vue组件
console.log('\n测试 3: 检查Vue组件');
console.log('═'.repeat(50));
try {
  const components = [
    { file: 'src/App.vue', name: 'App' },
    { file: 'src/components/MapView.vue', name: 'MapView' },
    { file: 'src/components/DevicePanel.vue', name: 'DevicePanel' }
  ];

  let allOk = true;
  components.forEach(comp => {
    const content = fs.readFileSync(path.join(__dirname, comp.file), 'utf-8');
    if (content.includes('<template>') && content.includes('<script')) {
      console.log(`[OK] ${comp.name} 组件结构正确`);
    } else {
      console.log(`[FAIL] ${comp.name} 组件结构不完整`);
      allOk = false;
    }
  });

  tests.push({ name: '检查Vue组件', passed: allOk });
} catch (e) {
  console.log(`[FAIL] 错误: ${e.message}`);
  tests.push({ name: '检查Vue组件', passed: false });
}

// 测试 4: 检查配置
console.log('\n测试 4: 检查配置');
console.log('═'.repeat(50));
try {
  const viteConfig = fs.readFileSync(path.join(__dirname, 'vite.config.js'), 'utf-8');

  const checks = [
    { pattern: 'defineConfig', name: 'Vite配置' },
    { pattern: '@vitejs/plugin-vue', name: 'Vue插件' },
    { pattern: 'port', name: '端口配置' }
  ];

  let allOk = true;
  checks.forEach(check => {
    if (viteConfig.includes(check.pattern)) {
      console.log(`[OK] ${check.name}`);
    } else {
      console.log(`[FAIL] ${check.name} 未配置`);
      allOk = false;
    }
  });

  tests.push({ name: '检查配置', passed: allOk });
} catch (e) {
  console.log(`[FAIL] 错误: ${e.message}`);
  tests.push({ name: '检查配置', passed: false });
}

// 总结
console.log('\n' + '═'.repeat(50));
console.log('测试总结');
console.log('═'.repeat(50));

const passed = tests.filter(t => t.passed).length;
const total = tests.length;

tests.forEach(test => {
  const status = test.passed ? '[OK]' : '[FAIL]';
  console.log(`${status} ${test.name}`);
});

console.log(`\n总体: ${passed}/${total} 测试通过`);

if (passed === total) {
  console.log('\n✓ 所有测试通过！前端已准备就绪。\n');
  process.exit(0);
} else {
  console.log(`\n✗ 有 ${total - passed} 个测试失败。\n`);
  process.exit(1);
}
