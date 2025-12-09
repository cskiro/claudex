#!/usr/bin/env node

/**
 * Test Template Generator
 *
 * Generates test file templates based on implementation files.
 * Analyzes project structure and test framework to create appropriate templates.
 */

const fs = require('fs');
const path = require('path');

function generateTest() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Usage: npm run generate:test <implementation-file>');
    console.error('');
    console.error('Example:');
    console.error('  npm run generate:test src/features/auth/login.ts');
    process.exit(1);
  }

  const implFile = args[0];

  if (!fs.existsSync(implFile)) {
    console.error(`❌ Error: File not found: ${implFile}`);
    process.exit(1);
  }

  // Determine test file path
  const ext = path.extname(implFile);
  const testFile = implFile.replace(ext, `.test${ext}`);

  if (fs.existsSync(testFile)) {
    console.error(`❌ Error: Test file already exists: ${testFile}`);
    console.error('   Use a different name or edit the existing file');
    process.exit(1);
  }

  // Get implementation file info
  const filename = path.basename(implFile, ext);
  const implContent = fs.readFileSync(implFile, 'utf-8');

  // Detect test framework
  const testFramework = detectTestFramework();

  // Generate appropriate template
  const template = generateTemplate(filename, implFile, implContent, testFramework);

  // Write test file
  fs.writeFileSync(testFile, template, 'utf-8');

  console.log('✅ Test file created:', testFile);
  console.log('');
  console.log('📝 Next steps:');
  console.log('  1. Edit the test file to add specific test cases');
  console.log('  2. Run tests to verify RED phase:');
  console.log(`     npm run test:red -- ${testFile}`);
  console.log('  3. Implement the feature');
  console.log('  4. Run tests to verify GREEN phase:');
  console.log(`     npm run test:green -- ${testFile}`);
}

function detectTestFramework() {
  const packageJsonPath = path.join(process.cwd(), 'package.json');

  if (!fs.existsSync(packageJsonPath)) {
    return 'vitest'; // default
  }

  try {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
    const allDeps = {
      ...packageJson.dependencies,
      ...packageJson.devDependencies
    };

    if (allDeps['vitest']) return 'vitest';
    if (allDeps['jest']) return 'jest';
    if (allDeps['@jest/globals']) return 'jest';
    if (allDeps['mocha']) return 'mocha';

    return 'vitest'; // default
  } catch (error) {
    return 'vitest';
  }
}

function generateTemplate(filename, implFile, implContent, testFramework) {
  const relativePath = path.relative(path.dirname(implFile), implFile);
  const importPath = './' + path.basename(implFile, path.extname(implFile));

  // Extract potential functions/classes to test
  const entities = extractEntities(implContent);

  let template = '';

  // Add imports based on test framework
  if (testFramework === 'vitest') {
    template += `import { describe, it, expect, beforeEach, afterEach } from 'vitest';\n`;
  } else if (testFramework === 'jest') {
    template += `import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';\n`;
  } else {
    template += `const { describe, it, expect, beforeEach, afterEach } = require('${testFramework}');\n`;
  }

  // Add import for implementation
  template += `import * as impl from '${importPath}';\n`;
  template += `\n`;

  // Add main describe block
  template += `describe('${filename}', () => {\n`;
  template += `  // TODO: Add setup and teardown if needed\n`;
  template += `  // beforeEach(() => {\n`;
  template += `  //   // Setup before each test\n`;
  template += `  // });\n`;
  template += `\n`;
  template += `  // afterEach(() => {\n`;
  template += `  //   // Cleanup after each test\n`;
  template += `  //   });\n`;
  template += `\n`;

  if (entities.length > 0) {
    // Generate test stubs for each entity
    entities.forEach(entity => {
      template += `  describe('${entity}', () => {\n`;
      template += `    it('should [behavior] when [condition]', () => {\n`;
      template += `      // Arrange\n`;
      template += `      // TODO: Set up test data and dependencies\n`;
      template += `\n`;
      template += `      // Act\n`;
      template += `      // TODO: Call the function/method being tested\n`;
      template += `      // const result = impl.${entity}();\n`;
      template += `\n`;
      template += `      // Assert\n`;
      template += `      // TODO: Verify the expected behavior\n`;
      template += `      expect(true).toBe(false); // Replace with actual assertion\n`;
      template += `    });\n`;
      template += `\n`;
      template += `    // TODO: Add more test cases:\n`;
      template += `    // it('should handle edge case when [condition]', () => { ... });\n`;
      template += `    // it('should throw error when [invalid input]', () => { ... });\n`;
      template += `  });\n`;
      template += `\n`;
    });
  } else {
    // Generic test template
    template += `  it('should [behavior] when [condition]', () => {\n`;
    template += `    // Arrange\n`;
    template += `    // TODO: Set up test data and dependencies\n`;
    template += `\n`;
    template += `    // Act\n`;
    template += `    // TODO: Call the function/method being tested\n`;
    template += `\n`;
    template += `    // Assert\n`;
    template += `    // TODO: Verify the expected behavior\n`;
    template += `    expect(true).toBe(false); // Replace with actual assertion\n`;
    template += `  });\n`;
    template += `\n`;
    template += `  // TODO: Add more test cases for different scenarios\n`;
  }

  template += `});\n`;

  return template;
}

function extractEntities(content) {
  const entities = [];

  // Extract exported functions
  const functionMatches = content.matchAll(/export\s+(?:async\s+)?function\s+([a-zA-Z0-9_]+)/g);
  for (const match of functionMatches) {
    entities.push(match[1]);
  }

  // Extract exported classes
  const classMatches = content.matchAll(/export\s+class\s+([a-zA-Z0-9_]+)/g);
  for (const match of classMatches) {
    entities.push(match[1]);
  }

  // Extract exported const functions (arrow functions)
  const constMatches = content.matchAll(/export\s+const\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?\(/g);
  for (const match of constMatches) {
    entities.push(match[1]);
  }

  return entities;
}

// Run if called directly
if (require.main === module) {
  generateTest();
}

module.exports = { generateTest };
