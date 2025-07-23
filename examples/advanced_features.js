#!/usr/bin/env node
/**
 * GPToggle Advanced Features Examples (JavaScript/Node.js)
 * 
 * Demonstrates advanced GPToggle capabilities including:
 * - UMID generation and management
 * - Cross-service module export
 * - Module lifecycle operations
 * - Advanced query analysis
 */

const fs = require('fs');
const path = require('path');

// Import UMID generator (TypeScript needs to be compiled first)
try {
    const { UMIDGenerator } = require('../modules/umidGenerator.ts');
} catch (e) {
    console.log('Note: TypeScript files need to be compiled for full functionality');
}

class GPToggleAdvancedDemo {
    constructor() {
        this.userProfile = {
            userId: 'demo-user',
            context: {
                modules: {}
            }
        };
    }

    async umidGenerationExample() {
        console.log('\n=== UMID Generation Example ===');
        
        try {
            // Simulate UMID generation (would use actual UMIDGenerator in practice)
            const umidExamples = [
                'gptoggle.list.a1b2c3d4.1721737200.x7z9',
                'myapp.planner.e5f6g7h8.1721737201.m3p5',
                'chatgpt.interest.i9j0k1l2.1721737202.q8w2'
            ];
            
            console.log('Generated UMID examples:');
            umidExamples.forEach(umid => {
                const parts = umid.split('.');
                console.log(`  ${umid}`);
                console.log(`    Service: ${parts[0]}`);
                console.log(`    Type: ${parts[1]}`);
                console.log(`    Context: ${parts[2]}`);
                console.log(`    Created: ${new Date(parseInt(parts[3]) * 1000).toISOString()}`);
                console.log(`    Random: ${parts[4]}`);
            });
            
        } catch (error) {
            console.log(`UMID generation requires TypeScript compilation: ${error.message}`);
        }
    }

    async moduleLifecycleExample() {
        console.log('\n=== Module Lifecycle Example ===');
        
        // Simulate module creation
        const newModule = {
            type: 'list',
            data: ['milk', 'eggs', 'bread'],
            metadata: {
                createdAt: new Date().toISOString(),
                lastUpdated: new Date().toISOString(),
                lastAccessed: new Date().toISOString(),
                priority: 7,
                tags: ['shopping', 'groceries'],
                archived: false
            }
        };
        
        const umid = 'gptoggle.list.60c096b2.1721737200.814f';
        this.userProfile.context.modules[umid] = newModule;
        
        console.log(`Created module: ${umid}`);
        console.log(`Type: ${newModule.type}`);
        console.log(`Items: ${newModule.data.length}`);
        console.log(`Priority: ${newModule.metadata.priority}`);
        
        // Simulate aging and cleanup
        const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
        const ninetyDaysAgo = new Date(Date.now() - 90 * 24 * 60 * 60 * 1000);
        
        console.log('\nModule lifecycle stages:');
        console.log(`Active phase: < 30 days (until ${thirtyDaysAgo.toDateString()})`);
        console.log(`Archive phase: 30-90 days`);
        console.log(`Cleanup phase: > 90 days (after ${ninetyDaysAgo.toDateString()})`);
    }

    async crossServiceExportExample() {
        console.log('\n=== Cross-Service Export Example ===');
        
        // Simulate export data
        const exportData = {
            source_service: 'gptoggle',
            target_service: 'notion',
            export_timestamp: new Date().toISOString(),
            modules: {}
        };
        
        // Add modules to export
        Object.entries(this.userProfile.context.modules).forEach(([umid, module]) => {
            exportData.modules[umid] = {
                original_umid: umid,
                type: module.type,
                data: module.data,
                metadata: {
                    ...module.metadata,
                    exported_from: 'gptoggle',
                    export_timestamp: new Date().toISOString()
                }
            };
        });
        
        console.log(`Exporting ${Object.keys(exportData.modules).length} modules to Notion`);
        console.log('Export format:');
        console.log(JSON.stringify(exportData, null, 2));
        
        // Save export file
        const exportPath = path.join(__dirname, 'export_data.json');
        fs.writeFileSync(exportPath, JSON.stringify(exportData, null, 2));
        console.log(`Export saved to: ${exportPath}`);
    }

    async batchOperationsExample() {
        console.log('\n=== Batch Operations Example ===');
        
        const batchQueries = [
            "Add cheese and yogurt to my shopping list",
            "Schedule gym session for tomorrow at 7 AM", 
            "I'm interested in learning about renewable energy",
            "Track my daily water intake - goal is 8 glasses"
        ];
        
        console.log('Processing batch queries:');
        const results = [];
        
        batchQueries.forEach((query, index) => {
            // Simulate query processing
            const result = {
                query: query,
                moduleActions: this.simulateModuleActions(query),
                timestamp: new Date().toISOString()
            };
            
            results.push(result);
            
            console.log(`\n${index + 1}. "${query}"`);
            console.log(`   Actions: ${result.moduleActions.length}`);
            result.moduleActions.forEach(action => {
                console.log(`   → ${action.action} ${action.moduleType} (${action.umid.substring(0, 20)}...)`);
            });
        });
        
        return results;
    }

    simulateModuleActions(query) {
        const actions = [];
        const timestamp = Math.floor(Date.now() / 1000);
        
        // Simple pattern matching for demo
        if (query.toLowerCase().includes('shopping') || query.toLowerCase().includes('list')) {
            actions.push({
                action: 'update',
                moduleType: 'list',
                umid: `gptoggle.list.60c096b2.${timestamp}.814f`,
                success: true
            });
        }
        
        if (query.toLowerCase().includes('schedule') || query.toLowerCase().includes('gym')) {
            actions.push({
                action: 'create',
                moduleType: 'calendar',
                umid: `gptoggle.calendar.7d8e9f0a.${timestamp}.y5u7`,
                success: true
            });
        }
        
        if (query.toLowerCase().includes('interested') || query.toLowerCase().includes('learning')) {
            actions.push({
                action: 'create',
                moduleType: 'interest',
                umid: `gptoggle.interest.b1c2d3e4.${timestamp}.i9o1`,
                success: true
            });
        }
        
        if (query.toLowerCase().includes('track') || query.toLowerCase().includes('goal')) {
            actions.push({
                action: 'create',
                moduleType: 'tracker',
                umid: `gptoggle.tracker.f5g6h7i8.${timestamp}.p3r5`,
                success: true
            });
        }
        
        return actions;
    }

    async analyticsExample() {
        console.log('\n=== Analytics Example ===');
        
        // Simulate analytics data
        const analytics = {
            totalModules: Object.keys(this.userProfile.context.modules).length,
            modulesByType: {
                list: 1,
                planner: 0,
                calendar: 0,
                interest: 0,
                tracker: 0,
                goal: 0
            },
            mostActiveType: 'list',
            averageModulesPerUser: 3.2,
            creationRate: 1.5, // per day
            retentionRate: 78.5 // percentage
        };
        
        console.log('Module Analytics:');
        console.log(`Total modules: ${analytics.totalModules}`);
        console.log(`Most active type: ${analytics.mostActiveType}`);
        console.log(`Average modules per user: ${analytics.averageModulesPerUser}`);
        console.log(`Daily creation rate: ${analytics.creationRate}`);
        console.log(`Retention rate: ${analytics.retentionRate}%`);
        
        console.log('\nModules by type:');
        Object.entries(analytics.modulesByType).forEach(([type, count]) => {
            if (count > 0) {
                console.log(`  ${type}: ${count}`);
            }
        });
    }

    async performanceExample() {
        console.log('\n=== Performance Example ===');
        
        const operations = [
            'Module creation',
            'Query analysis', 
            'Data extraction',
            'UMID generation',
            'Context analysis'
        ];
        
        console.log('Performance benchmarks:');
        operations.forEach(operation => {
            const startTime = Date.now();
            
            // Simulate operation
            setTimeout(() => {}, Math.random() * 10);
            
            const endTime = Date.now();
            const duration = endTime - startTime;
            
            console.log(`${operation}: ${duration}ms`);
        });
        
        console.log('\nTarget performance metrics:');
        console.log('• Module operations: < 10ms');
        console.log('• Query analysis: < 5ms');
        console.log('• Data extraction: 90%+ accuracy');
        console.log('• Memory efficiency: Minimal impact');
    }

    async errorHandlingExample() {
        console.log('\n=== Error Handling Example ===');
        
        const errorScenarios = [
            'Invalid UMID format',
            'Service not found',
            'Module type not supported',
            'Context hash collision',
            'Timestamp out of range'
        ];
        
        console.log('Error handling scenarios:');
        errorScenarios.forEach((scenario, index) => {
            console.log(`${index + 1}. ${scenario}`);
            console.log(`   → Graceful degradation with fallback`);
        });
        
        console.log('\nError recovery strategies:');
        console.log('• Fallback to default behavior');
        console.log('• Retry with exponential backoff');
        console.log('• User notification with options');
        console.log('• Log errors for analysis');
    }

    async runAllExamples() {
        console.log('GPToggle Advanced Features Demo (JavaScript)');
        console.log('=' .repeat(50));
        
        try {
            await this.umidGenerationExample();
            await this.moduleLifecycleExample();
            await this.crossServiceExportExample();
            await this.batchOperationsExample();
            await this.analyticsExample();
            await this.performanceExample();
            await this.errorHandlingExample();
            
            console.log('\n' + '='.repeat(50));
            console.log('✅ All advanced examples completed!');
            console.log('\nNext steps:');
            console.log('- Compile TypeScript files for full UMID functionality');
            console.log('- Check out module_demos.py for Python module examples');
            console.log('- Read docs/MODULE_GUIDE.md for comprehensive module documentation');
            
        } catch (error) {
            console.error(`\n❌ Error running advanced examples: ${error.message}`);
            console.log('Make sure you have:');
            console.log('- Node.js installed for JavaScript examples');
            console.log('- TypeScript compiled for UMID functionality');
            console.log('- Required dependencies installed');
        }
    }
}

// Run examples if called directly
if (require.main === module) {
    const demo = new GPToggleAdvancedDemo();
    demo.runAllExamples();
}

module.exports = GPToggleAdvancedDemo;