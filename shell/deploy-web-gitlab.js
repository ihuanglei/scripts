'use strict';

const packageConfig = require('../package.json')

const ora = require('ora')
const chalk = require('chalk')
const spinner = ora('building for release...')

const TOKEN = '';

const URL_UPLOAD='';

const URL_RELEASE=''

function exec (cmd) {
  return require('child_process')
    .execSync(cmd)
    .toString()
    .trim()
}

spinner.start()

const TAR_FILE = 'v' + packageConfig.version + '.tar.gz';

const CMD_TAR = 'tar czf ' + TAR_FILE + ' -C dist/ .';

let ret = exec(CMD_TAR)

const CMD_UPLOAD =
  'curl -s --request POST --header "PRIVATE-TOKEN: ' +
  TOKEN +
  '" --form "file=@' +
  TAR_FILE +
  '" '+ URL_UPLOAD;

ret = JSON.parse(exec(CMD_UPLOAD))

const CMD_TAG =
  'git tag -a v' + packageConfig.version + ' -m v' + packageConfig.version
exec(CMD_TAG)

const CMD_TAG_PUSH = 'git push origin v' + packageConfig.version
exec(CMD_TAG_PUSH)

const CMD_TAG_DEL = 'git tag -d v' + packageConfig.version
exec(CMD_TAG_DEL)

let data = '# Release v' + packageConfig.version + '\n' + ret.markdown

const CMD_RELEASE =
  'curl -s --request POST --header "PRIVATE-TOKEN: ' +
  TOKEN +
  '" --data "description=' +
  data +
  '" '+ URL_RELEASE;

ret = JSON.parse(exec(CMD_RELEASE))

spinner.stop()

console.log()
console.log(chalk.green(exec('npm --no-git-tag-version version patch')))

console.log()
console.log(chalk.cyan('Complete.\n'))
