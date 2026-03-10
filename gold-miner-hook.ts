// 黄金矿工钩子状态机 - TypeScript 实现

// ==================== 类型定义 ====================

// 物品类型
enum ItemType {
    NONE = 'none',          // 空
    GOLD_SMALL = 'gold_small',     // 小金块
    GOLD_MEDIUM = 'gold_medium',   // 中金块
    GOLD_LARGE = 'gold_large',     // 大金块
    STONE_SMALL = 'stone_small',   // 小石头
    STONE_MEDIUM = 'stone_medium', // 中石头
    STONE_LARGE = 'stone_large',   // 大石头
    DIAMOND = 'diamond',           // 钻石
    TNT = 'tnt'                    // TNT炸药
}

// 钩子状态
enum HookState {
    IDLE = 'idle',           // 待命
    SWINGING = 'swinging',   // 摆动
    SHOOTING = 'shooting',   // 发射
    GRABBING = 'grabbing',   // 抓取中
    RETRACTING = 'retracting' // 回收
}

// 物品属性
interface Item {
    type: ItemType;
    weight: number;      // 重量（影响回收速度）
    value: number;       // 价值
    size: number;        // 大小
}

// 钩子位置
interface Position {
    x: number;
    y: number;
    angle: number;
}

// 状态转换事件
interface StateTransition {
    from: HookState;
    to: HookState;
    reason: string;
}

// ==================== 物品配置 ====================

const ITEM_CONFIG: Record<ItemType, Item> = {
    [ItemType.NONE]: { type: ItemType.NONE, weight: 0, value: 0, size: 0 },
    [ItemType.GOLD_SMALL]: { type: ItemType.GOLD_SMALL, weight: 5, value: 100, size: 20 },
    [ItemType.GOLD_MEDIUM]: { type: ItemType.GOLD_MEDIUM, weight: 10, value: 250, size: 30 },
    [ItemType.GOLD_LARGE]: { type: ItemType.GOLD_LARGE, weight: 15, value: 500, size: 40 },
    [ItemType.STONE_SMALL]: { type: ItemType.STONE_SMALL, weight: 20, value: 11, size: 25 },
    [ItemType.STONE_MEDIUM]: { type: ItemType.STONE_MEDIUM, weight: 30, value: 20, size: 35 },
    [ItemType.STONE_LARGE]: { type: ItemType.STONE_LARGE, weight: 50, value: 35, size: 45 },
    [ItemType.DIAMOND]: { type: ItemType.DIAMOND, weight: 2, value: 600, size: 10 },
    [ItemType.TNT]: { type: ItemType.TNT, weight: 5, value: 0, size: 25 }
};

// ==================== 状态机类 ====================

class GoldMinerHookStateMachine {
    // 当前状态
    private currentState: HookState = HookState.IDLE;
    private previousState: HookState | null = null;

    // 钩子属性
    private position: Position = { x: 0, y: 0, angle: 0 };
    private velocity: number = 0;
    private maxVelocity: number = 10;
    private hookLength: number = 0;
    private maxHookLength: number = 300;

    // 摆动参数
    private swingAngle: number = 0;
    private swingDirection: number = 1;
    private swingSpeed: number = 2;
    private maxSwingAngle: number = 70;

    // 抓取的物品
    private grabbedItem: Item | null = null;
    private isExploding: boolean = false;

    // 统计信息
    private score: number = 0;
    private itemsCollected: number = 0;

    // 回调函数（用于外部监听）
    private onStateChange: (transition: StateTransition) => void = () => {};

    constructor() {
        this.enterIdle();
    }

    // ==================== 状态设置 ====================

    setStateChangeCallback(callback: (transition: StateTransition) => void): void {
        this.onStateChange = callback;
    }

    // ==================== 状态转换 ====================

    private transitionTo(newState: HookState, reason: string): void {
        if (this.currentState === newState) return;

        const transition: StateTransition = {
            from: this.currentState,
            to: newState,
            reason
        };

        this.previousState = this.currentState;
        this.onStateChange(transition);

        // 退出当前状态
        this.exitState(this.currentState);

        // 进入新状态
        this.currentState = newState;
        this.enterState(newState);
    }

    private enterState(state: HookState): void {
        switch (state) {
            case HookState.IDLE:
                this.enterIdle();
                break;
            case HookState.SWINGING:
                this.enterSwinging();
                break;
            case HookState.SHOOTING:
                this.enterShooting();
                break;
            case HookState.GRABBING:
                this.enterGrabbing();
                break;
            case HookState.RETRACTING:
                this.enterRetracting();
                break;
        }
    }

    private exitState(state: HookState): void {
        switch (state) {
            case HookState.IDLE:
                this.exitIdle();
                break;
            case HookState.SWINGING:
                this.exitSwinging();
                break;
            case HookState.SHOOTING:
                this.exitShooting();
                break;
            case HookState.GRABBING:
                this.exitGrabbing();
                break;
            case HookState.RETRACTING:
                this.exitRetracting();
                break;
        }
    }

    // ==================== IDLE 状态 ====================

    private enterIdle(): void {
        console.log('🎯 进入待命状态 (IDLE)');
        this.position = { x: 0, y: 0, angle: 0 };
        this.hookLength = 0;
        this.velocity = 0;
        this.grabbedItem = null;
        this.isExploding = false;
    }

    private exitIdle(): void {
        console.log('🚪 退出待命状态 (IDLE)');
    }

    public startSwinging(): boolean {
        if (this.currentState !== HookState.IDLE) {
            console.warn('⚠️ 只能从待命状态开始摆动');
            return false;
        }
        this.transitionTo(HookState.SWINGING, '玩家按下空格键开始摆动');
        return true;
    }

    // ==================== SWINGING 状态 ====================

    private enterSwinging(): void {
        console.log('🔄 进入摆动状态 (SWINGING)');
        this.swingAngle = -this.maxSwingAngle;
        this.swingDirection = 1;
    }

    private exitSwinging(): void {
        console.log('🚪 退出摆动状态 (SWINGING)');
    }

    public updateSwinging(): void {
        if (this.currentState !== HookState.SWINGING) return;

        // 更新摆动角度
        this.swingAngle += this.swingSpeed * this.swingDirection;

        // 边界检测
        if (this.swingAngle >= this.maxSwingAngle) {
            this.swingDirection = -1;
            this.swingAngle = this.maxSwingAngle;
        } else if (this.swingAngle <= -this.maxSwingAngle) {
            this.swingDirection = 1;
            this.swingAngle = -this.maxSwingAngle;
        }

        this.position.angle = this.swingAngle;
        console.log(`🎢 摆动角度: ${this.swingAngle.toFixed(1)}°`);
    }

    public shoot(): boolean {
        if (this.currentState !== HookState.SWINGING) {
            console.warn('⚠️ 只能在摆动状态发射钩子');
            return false;
        }
        this.transitionTo(HookState.SHOOTING, '玩家按下发射键');
        return true;
    }

    // ==================== SHOOTING 状态 ====================

    private enterShooting(): void {
        console.log('🚀 进入发射状态 (SHOOTING)');
        this.velocity = this.maxVelocity;
    }

    private exitShooting(): void {
        console.log('🚪 退出发射状态 (SHOOTING)');
    }

    public updateShooting(): void {
        if (this.currentState !== HookState.SHOOTING) return;

        // 更新钩子位置
        this.hookLength += this.velocity;

        // 计算钩子坐标
        const rad = this.position.angle * Math.PI / 180;
        this.position.x = Math.sin(rad) * this.hookLength;
        this.position.y = Math.cos(rad) * this.hookLength;

        console.log(`📏 钩子长度: ${this.hookLength.toFixed(1)} / ${this.maxHookLength}`);

        // 检查是否达到最大长度
        if (this.hookLength >= this.maxHookLength) {
            console.log('🚫 钩子达到最大长度，开始回收');
            this.transitionTo(HookState.RETRACTING, '钩子达到最大长度');
        }
    }

    public checkCollision(itemType: ItemType): boolean {
        if (this.currentState !== HookState.SHOOTING) {
            console.warn('⚠️ 只能在发射状态检测碰撞');
            return false;
        }

        const item = ITEM_CONFIG[itemType];

        // 处理TNT特殊情况
        if (itemType === ItemType.TNT) {
            console.log('💥 钩子碰到TNT，触发爆炸！');
            this.isExploding = true;
            this.transitionTo(HookState.RETRACTING, '碰到TNT炸药');
            return true;
        }

        // 抓取物品
        this.grabbedItem = item;
        console.log(`🎣 抓到物品: ${itemType} (重量: ${item.weight}, 价值: ${item.value})`);

        this.transitionTo(HookState.GRABBING, `抓到${itemType}`);
        return true;
    }

    // ==================== GRABBING 状态 ====================

    private enterGrabbing(): void {
        console.log('✨ 进入抓取中状态 (GRABBING)');
        
        // 根据物品重量确定抓取时间
        let grabTime = 500; // 默认500ms
        if (this.grabbedItem) {
            // 石头需要更长的抓取时间
            if (this.grabbedItem.type.includes('stone')) {
                grabTime = 1000 + this.grabbedItem.weight * 50;
            } else if (this.grabbedItem.type === ItemType.DIAMOND) {
                grabTime = 200; // 钻石很快
            }
        }

        console.log(`⏱️ 抓取时间: ${grabTime}ms`);

        // 模拟抓取完成后自动转换
        setTimeout(() => {
            if (this.currentState === HookState.GRABBING) {
                console.log('✅ 抓取完成，开始回收');
                this.transitionTo(HookState.RETRACTING, '抓取完成');
            }
        }, grabTime);
    }

    private exitGrabbing(): void {
        console.log('🚪 退出抓取中状态 (GRABBING)');
    }

    // ==================== RETRACTING 状态 ====================

    private enterRetracting(): void {
        console.log('🔄 进入回收状态 (RETRACTING)');

        // 根据物品重量计算回收速度
        let baseRetractSpeed = this.maxVelocity;
        if (this.grabbedItem) {
            // 石头回收很慢，金块中等，钻石很快
            if (this.grabbedItem.type.includes('stone')) {
                baseRetractSpeed = Math.max(1, this.maxVelocity - this.grabbedItem.weight * 0.3);
            } else if (this.grabbedItem.type.includes('gold')) {
                baseRetractSpeed = Math.max(3, this.maxVelocity - this.grabbedItem.weight * 0.5);
            } else if (this.grabbedItem.type === ItemType.DIAMOND) {
                baseRetractSpeed = this.maxVelocity;
            }
        } else if (this.isExploding) {
            // TNT爆炸后快速回收
            baseRetractSpeed = this.maxVelocity * 1.5;
        }

        this.velocity = baseRetractSpeed;
        console.log(`🚗 回收速度: ${this.velocity.toFixed(2)}`);
    }

    private exitRetracting(): void {
        console.log('🚪 退出回收状态 (RETRACTING)');
        
        // 结算物品
        if (this.grabbedItem && !this.isExploding) {
            this.score += this.grabbedItem.value;
            this.itemsCollected++;
            console.log(`💰 收集物品: ${this.grabbedItem.type} (+${this.grabbedItem.value}分)`);
            console.log(`📊 当前总分: ${this.score}`);
        }
        
        this.grabbedItem = null;
        this.isExploding = false;
    }

    public updateRetracting(): void {
        if (this.currentState !== HookState.RETRACTING) return;

        // 更新钩子位置
        this.hookLength -= this.velocity;

        // 计算钩子坐标
        const rad = this.position.angle * Math.PI / 180;
        this.position.x = Math.sin(rad) * this.hookLength;
        this.position.y = Math.cos(rad) * this.hookLength;

        console.log(`🔄 回收中... 剩余长度: ${this.hookLength.toFixed(1)}`);

        // 检查是否回收完成
        if (this.hookLength <= 0) {
            this.hookLength = 0;
            console.log('✅ 回收完成');
            this.transitionTo(HookState.IDLE, '回收完成');
        }
    }

    // ==================== 辅助方法 ====================

    public getCurrentState(): HookState {
        return this.currentState;
    }

    public getPosition(): Position {
        return { ...this.position };
    }

    public getGrabbedItem(): Item | null {
        return this.grabbedItem;
    }

    public getScore(): number {
        return this.score;
    }

    public getItemsCollected(): number {
        return this.itemsCollected;
    }

    public isExplodingTNT(): boolean {
        return this.isExploding;
    }
}

// ==================== 演示代码 ====================

// 模拟延迟函数
function delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 状态变更监听器
function onStateChange(transition: StateTransition): void {
    console.log(`\n⚡ 状态转换: ${transition.from} ➜ ${transition.to}`);
    console.log(`   原因: ${transition.reason}\n`);
}

// 演示函数
async function demo(): Promise<void> {
    console.log('========================================');
    console.log('🎮 黄金矿工钩子状态机演示');
    console.log('========================================\n');

    const hook = new GoldMinerHookStateMachine();
    hook.setStateChangeCallback(onStateChange);

    // 场景1: 抓取中金块
    console.log('\n📜 场景1: 抓取中金块\n');
    console.log('--- 待命 ---');
    hook.startSwinging();

    // 模拟摆动
    for (let i = 0; i < 5; i++) {
        hook.updateSwinging();
        await delay(200);
    }

    console.log('\n--- 发射 ---');
    hook.shoot();

    // 模拟发射
    while (hook.getCurrentState() === HookState.SHOOTING) {
        hook.updateShooting();
        // 在某个距离模拟碰撞
        if (hook.getPosition().y > 100) {
            console.log('💥 碰撞检测: 中金块');
            hook.checkCollision(ItemType.GOLD_MEDIUM);
            break;
        }
        await delay(100);
    }

    // 等待抓取完成（自动转换）
    await delay(600);

    // 模拟回收
    while (hook.getCurrentState() === HookState.RETRACTING) {
        hook.updateRetracting();
        await delay(100);
    }

    // 场景2: 抓取大石头
    console.log('\n\n📜 场景2: 抓取大石头（很重！）\n');
    console.log('--- 待命 ---');
    hook.startSwinging();

    for (let i = 0; i < 5; i++) {
        hook.updateSwinging();
        await delay(200);
    }

    console.log('\n--- 发射 ---');
    hook.shoot();

    while (hook.getCurrentState() === HookState.SHOOTING) {
        hook.updateShooting();
        if (hook.getPosition().y > 100) {
            console.log('💥 碰撞检测: 大石头');
            hook.checkCollision(ItemType.STONE_LARGE);
            break;
        }
        await delay(100);
    }

    await delay(1500); // 大石头抓取时间长

    while (hook.getCurrentState() === HookState.RETRACTING) {
        hook.updateRetracting();
        await delay(150); // 大石头回收慢，所以这里延迟长一点
    }

    // 场景3: 抓取钻石
    console.log('\n\n📜 场景3: 抓取钻石（快速！）\n');
    console.log('--- 待命 ---');
    hook.startSwinging();

    for (let i = 0; i < 5; i++) {
        hook.updateSwinging();
        await delay(200);
    }

    console.log('\n--- 发射 ---');
    hook.shoot();

    while (hook.getCurrentState() === HookState.SHOOTING) {
        hook.updateShooting();
        if (hook.getPosition().y > 100) {
            console.log('💥 碰撞检测: 钻石');
            hook.checkCollision(ItemType.DIAMOND);
            break;
        }
        await delay(100);
    }

    await delay(250); // 钻石很快

    while (hook.getCurrentState() === HookState.RETRACTING) {
        hook.updateRetracting();
        await delay(50); // 钻石回收很快
    }

    // 场景4: 碰到TNT
    console.log('\n\n📜 场景4: 碰到TNT炸药\n');
    console.log('--- 待命 ---');
    hook.startSwinging();

    for (let i = 0; i < 5; i++) {
        hook.updateSwinging();
        await delay(200);
    }

    console.log('\n--- 发射 ---');
    hook.shoot();

    while (hook.getCurrentState() === HookState.SHOOTING) {
        hook.updateShooting();
        if (hook.getPosition().y > 100) {
            console.log('💥 碰撞检测: TNT');
            hook.checkCollision(ItemType.TNT);
            break;
        }
        await delay(100);
    }

    while (hook.getCurrentState() === HookState.RETRACTING) {
        hook.updateRetracting();
        await delay(80);
    }

    // 场景5: 钩子达到最大长度（空钩）
    console.log('\n\n📜 场景5: 钩子达到最大长度（空钩）\n');
    console.log('--- 待命 ---');
    hook.startSwinging();

    for (let i = 0; i < 5; i++) {
        hook.updateSwinging();
        await delay(200);
    }

    console.log('\n--- 发射 ---');
    hook.shoot();

    while (hook.getCurrentState() === HookState.SHOOTING) {
        hook.updateShooting();
        // 不触发碰撞，让钩子达到最大长度
        await delay(100);
    }

    while (hook.getCurrentState() === HookState.RETRACTING) {
        hook.updateRetracting();
        await delay(80);
    }

    // 总结
    console.log('\n========================================');
    console.log('📊 演示总结');
    console.log('========================================');
    console.log(`💰 总得分: ${hook.getScore()}`);
    console.log(`📦 收集物品数: ${hook.getItemsCollected()}`);
    console.log('\n✨ 状态机演示完成！');
}

// 运行演示
if (require.main === module) {
    demo().catch(console.error);
}

// 导出模块
export { GoldMinerHookStateMachine, HookState, ItemType, Item, Position, StateTransition };