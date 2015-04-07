module.exports = function (grunt) {

    // 1. All configuration goes here
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        concat: {
            basic: {
                src: [
                    './bower_components/bootstrap/dist/css/bootstrap.min.css',
                    './bower_components/bootstrap/dist/css/bootstrap-theme.min.css',
                    './bower_components/bootstrap-datepicker-eyecon/css/datepicker.css',
                    'assets/src/style.css'
                ],
                dest: 'assets/production.css'
            }
        },
        uglify: {
            basic: {
                options: {
                    sourceMap: true
                },
                files: {
                    'assets/production.min.js': [
                        './bower_components/jquery/dist/jquery.min.js',
                        './bower_components/bootstrap/dist/js/bootstrap.min.js',
                        './bower_components/bootstrap-datepicker-eyecon/js/bootstrap-datepicker.js',
                        'assets/src/script.js'
                    ]
                }
            }
        }

    });

    // 3. Where we tell Grunt we plan to use this plug-in.
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-concat');

    // 4. Where we tell Grunt what to do when we type "grunt" into the terminal.
    grunt.registerTask('default', ['concat', 'uglify']);

};