#!/usr/bin/env node

/**
 * Project Type Detector
 *
 * Detects project type and test framework to provide appropriate TDD configuration.
 */

const fs = require('fs');
const path = require('path');

class ProjectDetector {
  constructor(projectRoot) {
    this.projectRoot = projectRoot;
    this.packageJsonPath = path.join(projectRoot, 'package.json');
  }

  /**
   * Detect project configuration
   * @returns {object} Project details
   */
  detect() {
    const result = {
      type: 'unknown',
      testFramework: 'unknown',
      hasPackageJson: false,
      hasGit: false,
      hasTypeScript: false,
      projectName: path.basename(this.projectRoot),
      recommendations: []
    };

    // Check for package.json
    if (fs.existsSync(this.packageJsonPath)) {
      result.hasPackageJson = true;
      this.analyzePackageJson(result);
    }

    // Check for git
    if (fs.existsSync(path.join(this.projectRoot, '.git'))) {
      result.hasGit = true;
    } else {
      result.recommendations.push('Initialize git repository for version control');
    }

    // Check for TypeScript
    if (fs.existsSync(path.join(this.projectRoot, 'tsconfig.json'))) {
      result.hasTypeScript = true;
    }

    // Detect project type
    result.type = this.detectProjectType(result);

    // Add recommendations
    if (result.testFramework === 'unknown') {
      result.recommendations.push('Install a test framework (vitest recommended)');
    }

    return result;
  }

  /**
   * Analyze package.json for dependencies and scripts
   * @param {object} result - Result object to populate
   */
  analyzePackageJson(result) {
    try {
      const packageJson = JSON.parse(fs.readFileSync(this.packageJsonPath, 'utf-8'));

      result.projectName = packageJson.name || result.projectName;

      const allDeps = {
        ...packageJson.dependencies,
        ...packageJson.devDependencies
      };

      // Detect test framework
      if (allDeps['vitest']) {
        result.testFramework = 'vitest';
      } else if (allDeps['jest']) {
        result.testFramework = 'jest';
      } else if (allDeps['mocha']) {
        result.testFramework = 'mocha';
      } else if (allDeps['ava']) {
        result.testFramework = 'ava';
      }

      // Detect framework/type
      if (allDeps['react']) {
        result.framework = 'react';
      } else if (allDeps['vue']) {
        result.framework = 'vue';
      } else if (allDeps['@angular/core']) {
        result.framework = 'angular';
      } else if (allDeps['express']) {
        result.framework = 'express';
      } else if (allDeps['fastify']) {
        result.framework = 'fastify';
      } else if (allDeps['next']) {
        result.framework = 'next';
      }

      // Check for existing test scripts
      result.hasTestScript = packageJson.scripts && packageJson.scripts.test;

    } catch (error) {
      console.error('Error parsing package.json:', error.message);
    }
  }

  /**
   * Determine primary project type
   * @param {object} result - Detection results
   * @returns {string} Project type
   */
  detectProjectType(result) {
    if (result.framework === 'react') return 'react';
    if (result.framework === 'vue') return 'vue';
    if (result.framework === 'angular') return 'angular';
    if (result.framework === 'next') return 'nextjs';
    if (result.framework === 'express' || result.framework === 'fastify') return 'nodejs-backend';
    if (result.hasTypeScript) return 'typescript';
    if (result.hasPackageJson) return 'nodejs';
    return 'unknown';
  }

  /**
   * Get recommended test command for project
   * @returns {string} Test command
   */
  getTestCommand() {
    const result = this.detect();

    switch (result.testFramework) {
      case 'vitest':
        return 'vitest --run';
      case 'jest':
        return 'jest';
      case 'mocha':
        return 'mocha';
      case 'ava':
        return 'ava';
      default:
        return 'npm test';
    }
  }

  /**
   * Get recommended test file extension
   * @returns {string} File extension
   */
  getTestExtension() {
    const result = this.detect();

    if (result.hasTypeScript) {
      return '.test.ts';
    }

    return '.test.js';
  }
}

module.exports = ProjectDetector;
