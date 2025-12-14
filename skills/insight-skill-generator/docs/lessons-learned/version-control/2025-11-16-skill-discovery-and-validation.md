# Version-control Insights - November 16, 2025

Auto-generated lessons learned from Claude Code Explanatory insights.

**Session**: 79b654b6-10f8-4c3c-92e1-a3535644366c
**Generated**: 2025-11-16 09:57:31

---

 valid YAML between `---` delimiters
2. **Required fields** - `name` and `description` must be present and valid
3. **Name format** - Lowercase kebab-case, max 64 chars
4. **Description format** - Max 1024 chars, contains action verbs

By validating these before even attempting to load the skill, we catch 90%+ of skill loading issues early.



---

## Skill Discovery and Validation

**Skill Discovery and Validation**

Claude Code skills are discovered by reading the frontmatter of SKILL.md files. The key validation points are:
1. **YAML syntax** - Must be valid YAML between `---` delimiters
2. **Required fields** - `name` and `description` must be present and valid
3. **Name format** - Lowercase kebab-case, max 64 chars
4. **Description format** - Max 1024 chars, contains action verbs

By validating these before even attempting to load the skill, we catch 90%+ of skill loading issues early.



---

## Skill Discovery and Validation

**Skill Discovery and Validation**

Claude Code skills are discovered by reading the frontmatter of SKILL.md files. The key validation points are:
1. **YAML syntax** - Must be valid YAML between `---` delimiters
2. **Required fields** - `name` and `description` must be present and valid
3. **Name format** - Lowercase kebab-case, max 64 chars
4. **Description format** - Max 1024 chars, contains action verbs

By validating these before even attempting to load the skill, we catch 90%+ of skill loading issues early.



---

## Skill as Documentation Pattern

**Skill as Documentation Pattern**

Notice that this skill doesn't execute code—it provides comprehensive instructions that I (Claude) interpret. The templates use Jinja2-style syntax for documentation reference, not programmatic rendering. This "skill as documentation" pattern is powerful because:

1. **Flexibility**: I can adapt instructions to context rather than rigidly executing code
2. **Maintainability**: Plain markdown is easier to update than code
3. **Clarity**: Users can read SKILL.md to understand exactly what will happen
4. **Extensibility**: Easy to add new phases, patterns, or validations

The configuration files (YAML) provide tunable parameters, while SKILL.md provides the logic I execute. This separation of concerns makes the skill both powerful and maintainable.



---

## Skill as Documentation Pattern

**Skill as Documentation Pattern**

Notice that this skill doesn't execute code—it provides comprehensive instructions that I (Claude) interpret. The templates use Jinja2-style syntax for documentation reference, not programmatic rendering. This "skill as documentation" pattern is powerful because:

1. **Flexibility**: I can adapt instructions to context rather than rigidly executing code
2. **Maintainability**: Plain markdown is easier to update than code
3. **Clarity**: Users can read SKILL.md to understand exactly what will happen
4. **Extensibility**: Easy to add new phases, patterns, or validations

The configuration files (YAML) provide tunable parameters, while SKILL.md provides the logic I execute. This separation of concerns makes the skill both powerful and maintainable.



---

## Skill as Documentation Pattern

**Skill as Documentation Pattern**

Notice that this skill doesn't execute code—it provides comprehensive instructions that I (Claude) interpret. The templates use Jinja2-style syntax for documentation reference, not programmatic rendering. This "skill as documentation" pattern is powerful because:

1. **Flexibility**: I can adapt instructions to context rather than rigidly executing code
2. **Maintainability**: Plain markdown is easier to update than code
3. **Clarity**: Users can read SKILL.md to understand exactly what will happen
4. **Extensibility**: Easy to add new phases, patterns, or validations

The configuration files (YAML) provide tunable parameters, while SKILL.md provides the logic I execute. This separation of concerns makes the skill both powerful and maintainable.



---

## Skill as Documentation Pattern

**Skill as Documentation Pattern**

Notice that this skill doesn't execute code—it provides comprehensive instructions that I (Claude) interpret. The templates use Jinja2-style syntax for documentation reference, not programmatic rendering. This "skill as documentation" pattern is powerful because:

1. **Flexibility**: I can adapt instructions to context rather than rigidly executing code
2. **Maintainability**: Plain markdown is easier to update than code
3. **Clarity**: Users can read SKILL.md to understand exactly what will happen
4. **Extensibility**: Easy to add new phases, patterns, or validations

The configuration files (YAML) provide tunable parameters, while SKILL.md provides the logic I execute. This separation of concerns makes the skill both powerful and maintainable.



---

## Skill as Documentation Pattern

**Skill as Documentation Pattern**

Notice that this skill doesn't execute code—it provides comprehensive instructions that I (Claude) interpret. The templates use Jinja2-style syntax for documentation reference, not programmatic rendering. This "skill as documentation" pattern is powerful because:

1. **Flexibility**: I can adapt instructions to context rather than rigidly executing code
2. **Maintainability**: Plain markdown is easier to update than code
3. **Clarity**: Users can read SKILL.md to understand exactly what will happen
4. **Extensibility**: Easy to add new phases, patterns, or validations

The configuration files (YAML) provide tunable parameters, while SKILL.md provides the logic I execute. This separation of concerns makes the skill both powerful and maintainable.



---

## Skill as Documentation Pattern

**Skill as Documentation Pattern**

Notice that this skill doesn't execute code—it provides comprehensive instructions that I (Claude) interpret. The templates use Jinja2-style syntax for documentation reference, not programmatic rendering. This "skill as documentation" pattern is powerful because:

1. **Flexibility**: I can adapt instructions to context rather than rigidly executing code
2. **Maintainability**: Plain markdown is easier to update than code
3. **Clarity**: Users can read SKILL.md to understand exactly what will happen
4. **Extensibility**: Easy to add new phases, patterns, or validations

The configuration files (YAML) provide tunable parameters, while SKILL.md provides the logic I execute. This separation of concerns makes the skill both powerful and maintainable.



---

