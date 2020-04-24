const width = 600;
const height = 480;
const speed = 110;
const config = {
    type: Phaser.WEBGL,
    width: width,
    height: height,
    scene: {
        preload: preload,
        create: create,
        update: update
    },
    physics: {
        default: 'arcade',
        arcade: {
            debug: false
        }
    },
    //pixelArt: true,
    zoom: 1
};

const tilesize = 16;
let offsetX = 0;
let offsetY = 0;

var game = new Phaser.Game(config);

var chr = {
    helth: 100,
    x: height/2,
    y: width/2,
    facing: "down",
    ammo: 12
}

var tree = {
    key: 'Tree1',
    x: height/3,
    y: width/3
}
var trees;
var bullets;
var player;
var helthText;
var ammoText;

function bulletTreeCollision(bullet, tree){
    bullet.disableBody(true, true)
}

function treeDamage(player, tree){
    console.log(player)
    chr.helth -= 1;
    helthText.setText('helth: '+chr.helth)
}

function preload() {
    this.load.image('Grass', 'assets/Grass.png');
    this.load.image('Tree1', 'assets/Tree1.png');
    this.load.image('Tree2', 'assets/Tree2.png');
    this.load.image('Tree3', 'assets/Tree3.png');
    this.load.image('Sea',   'assets/Sea.png');
    this.load.image('Boat1', 'assets/Boat1.png');
    this.load.image('Boat2', 'assets/Boat2.png');
    this.load.image('Sand',  'assets/Sand.png');
    this.load.image('Bomb',  'assets/bomb.png');
    this.load.image('inventory',  'assets/inventory.png');
    this.load.image('fist',  'assets/fist.png');
    this.load.image('arrow', 'assets/arrow.png')
    this.load.spritesheet('dude', 'assets/character.png', { frameWidth: 32, frameHeight: 32 });
    //noise.seed(Math.random());
    //cursors = this.input.keyboard.createCursorKeys();
    cursors = this.input.keyboard.addKeys(
        {
            up:Phaser.Input.Keyboard.KeyCodes.W,
            down:Phaser.Input.Keyboard.KeyCodes.S,
            left:Phaser.Input.Keyboard.KeyCodes.A,
            right:Phaser.Input.Keyboard.KeyCodes.D,
    });
    spaceBar = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
    spaceBar.on('down', shoot)
}

function shoot(){
    ammoText.setText('ammo: '+chr.ammo)
    if(chr.ammo <= 0){
        return
    }
    chr.ammo -= 1
    var dir = chr.facing
    console.log("shoot")
    var b = bullets.create(player.x, player.y, 'Bomb');
    b.setScale(0.5)
    setTimeout(function(){
        console.log("bullet timeout")
        console.log(b)
        b.setActive(false);
        b.setVisible(false);
        b.body.stop();
    }, 1000)
    var bspeed = speed *3
    if(dir === "up"){
        b.setVelocityY(-bspeed) 
    } else if (dir === "down"){
        b.setVelocityY(bspeed) 
    } else if (dir === "right"){
        b.setVelocityX(bspeed) 
    } else if (dir === "left"){
        b.setVelocityX(-bspeed) 
    }
}

function create() {
    //scene.add.displayList.removeAll();
    for (let y = 0; y < (height / tilesize); y++) {
        for (let x = 0; x < (width / tilesize); x++) {
            let posX = (x * tilesize) + 8;
            let posY = (y * tilesize) + 8;
                this.make.image({
                    x: posX,
                    y: posY,
                    key: 'Grass',
                    add: true
                });
        }
    }
    helthText = this.add.text(16, 16, 'helth: '+chr.helth, { fontSize: '16px', fill: '#000' });
    ammoText = this.add.text(16, 32, 'ammo: '+chr.ammo, { fontSize: '16px', fill: '#000' });

    trees = this.physics.add.staticGroup();
    bullets = this.physics.add.group();
    for(var i = 0;i< 10; i++){
        x = Math.floor(Math.random() * width) + 1;
        y = Math.floor(Math.random() * height) + 1;
        console.log(x, ",", y)
        t = trees.create(x, y, tree.key);
        t.setScale(2)
    }
    
    player = this.physics.add.sprite(chr.x, chr.y, 'dude')
    player.setCollideWorldBounds(true);
    //player.setBounce(2)
    this.physics.add.collider(player, trees);
    //this.physics.add.collider(bullets, trees)
    this.physics.add.collider(bullets, trees, bulletTreeCollision, null, this);
    //this.physics.add.overlap(player, trees, treeDamage, null, this);
    this.anims.create({
        key: 'left',
        frames: this.anims.generateFrameNumbers('dude', {frames:[3, 7, 11, 15]}),
        frameRate: 10,
        repeat: -1
    });
    
    this.anims.create({
        key: 'turn',
        frames: [ { key: 'dude', frame: 0 } ],
        frameRate: 20
    });
    
    this.anims.create({
        key: 'right',
        frames: this.anims.generateFrameNumbers('dude', {frames:[2, 6, 10, 14]}),
        frameRate: 10,
        repeat: -1
    });
    this.anims.create({
        key: 'up',
        frames: this.anims.generateFrameNumbers('dude', {frames:[1, 5, 9, 13]}),
        frameRate: 10,
        repeat: -1
    });
    this.anims.create({
        key: 'down',
        frames: this.anims.generateFrameNumbers('dude', {frames:[0, 4, 8, 12]}),
        frameRate: 10,
        repeat: -1
    });
    draw(this);
}

function update() {
    var moving = false
    // if (cursors.space.isDown){
    //     shoot(chr.facing)
    // }
    if (cursors.left.isDown) { 
        moving = true
        player.setVelocityX(-speed) 
        chr.facing = "left"
        player.anims.play('left', true);
    }
    if (cursors.right.isDown) { 
        moving = true
        player.setVelocityX(speed) 
        chr.facing = "right"
        player.anims.play('right', true);
    }
    if (cursors.up.isDown) { 
        moving = true
        player.setVelocityY(-speed)
        chr.facing = "up"
        player.anims.play('up', true);
    }
    if (cursors.down.isDown) { 
        moving = true
        player.setVelocityY(speed); 
        chr.facing = "down"
        player.anims.play('down', true);
    }
    if(!moving) {
        player.setVelocityX(0); player.setVelocityY(0)
        //player.anims.play('turn');
        player.anims.pause()
    }
    draw(this);
}

function draw(scene) {
    // scene.add.image(tree.x, tree.y, tree.key);
    scene.add.image(width/2, height-18, 'inventory');
    scene.add.image(width/2-64, height-18, 'fist');
    scene.add.image(width/2-32, height-18, 'Bomb')
    scene.add.image(width/2-64, height-50, 'arrow')
}

function between(value1, value2, value3) {
    return (value2 < value1 && value1 < value3)
}