# JSON Schema Limitations Reference

## Supported Features

- ✅ All basic types (object, array, string, integer, number, boolean, null)
- ✅ `enum` (primitives only)
- ✅ `const`, `anyOf`, `allOf`
- ✅ `$ref`, `$def`, `definitions` (local)
- ✅ `required`, `additionalProperties: false`
- ✅ String formats: date-time, time, date, email, uri, uuid, ipv4, ipv6
- ✅ `minItems: 0` or `minItems: 1` for arrays

## NOT Supported

- ❌ Recursive schemas
- ❌ Numerical constraints (minimum, maximum, multipleOf)
- ❌ String constraints (minLength, maxLength, pattern with complex regex)
- ❌ Array constraints (beyond minItems 0/1)
- ❌ External `$ref`
- ❌ Complex types in enums

## SDK Transformation

Python and TypeScript SDKs automatically remove unsupported constraints and add them to descriptions.

## Success Criteria

- [ ] Schema designed with all required fields
- [ ] JSON Schema limitations respected
- [ ] SDK helper integrated (Pydantic/Zod)
- [ ] Beta header included in requests
- [ ] Error handling for refusals and token limits
- [ ] Tested with representative examples
- [ ] Edge cases covered (missing fields, invalid data)
- [ ] Production optimization considered (caching, tokens)
- [ ] Monitoring in place (latency, costs)
- [ ] Documentation provided

## Important Reminders

1. **Use SDK helpers** - `client.beta.messages.parse()` auto-validates
2. **Respect limitations** - No recursive schemas, no min/max constraints
3. **Add descriptions** - Helps Claude understand what to extract
4. **Handle refusals** - Don't retry safety refusals
5. **Monitor performance** - Watch for cache misses and high latency
6. **Set `additionalProperties: false`** - Required for all objects
7. **Test thoroughly** - Edge cases often reveal schema issues
