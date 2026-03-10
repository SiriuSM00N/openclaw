// 黄金矿工钩子状态机实现
// 定义钩子状态枚举
enum HookState {
  IDLE = 'idle',           // 待命状态
  SWINGING = 'swinging',   // 摆动状态
  LAUNCHING = 'launching', // 发射状态
  RETRIEVING = 'retrieving', // 回收状态
  GRABBING = 'grabbing'    // 抓取状态
}

// 定义可抓取物品类型
enum GrabbableItemType {
  GOLD = 'gold',      // 金块
  STONE = 'stone',    // 石头
  EMPTY = 'empty'     // 空气（没有物品）
}

// 可抓取物品类
class GrabbableItem {
  type: GrabbableItemType;
  weight: number;      // 物品重量，影响钩子的拉力
  value: number;       // 物品价值

  constructor(type: GrabbableItemType, weight: number, value: number) {
    this.type = type;
    this.weight = weight;
    this.value = value;
  }
}

// 钩子状态接口
interface IHookState {
  enter(hook: HookStateMachine): void;
  execute(hook: HookStateMachine): void;
  exit(hook: HookStateMachine): void;
}

// 待命状态
class IdleState implements IHookState {
  enter(hook: HookStateMachine): void {
    console.log('钩子进入待命状态');
    hook.currentAngle = hook.initialAngle;
    hook.hookPosition = { x: hook.baseX, y: hook.baseY };
    hook.velocity = { x: 0, y: 0 };
    hook.isSwinging = false;
    hook.isLaunched = false;
  }

  execute(hook: HookStateMachine): void {
    // 在待命状态下，等待发射指令
    // 这里可以检测玩家输入
    if (hook.shouldLaunch) {
      hook.changeState(HookState.SWINGING);
    }
  }

  exit(hook: HookStateMachine): void {
    console.log('钩子退出待命状态');
  }
}

// 摆动状态
class SwingingState implements IHookState {
  private swingTimer: number = 0;
  
  enter(hook: HookStateMachine): void {
    console.log('钩子进入摆动状态');
    hook.isSwinging = true;
    this.swingTimer = 0;
    
    // 开始随机摆动
    hook.currentAngle = hook.initialAngle + Math.sin(this.swingTimer * 0.1) * 0.2;
    hook.updateHookPosition();
  }

  execute(hook: HookStateMachine): void {
    this.swingTimer += 0.1;
    
    // 模拟摆动效果
    hook.currentAngle = hook.initialAngle + Math.sin(this.swingTimer * 0.5) * 0.3;
    hook.updateHookPosition();
    
    // 检测是否发射
    if (hook.shouldLaunch) {
      hook.changeState(HookState.LAUNCHING);
    }
  }

  exit(hook: HookStateMachine): void {
    console.log('钩子退出摆动状态');
    hook.isSwinging = false;
  }
}

// 发射状态
class LaunchingState implements IHookState {
  enter(hook: HookStateMachine): void {
    console.log('钩子进入发射状态');
    hook.isLaunched = true;
    
    // 设置发射速度和方向
    const radians = hook.currentAngle * Math.PI / 180;
    hook.velocity = {
      x: Math.cos(radians) * hook.launchSpeed,
      y: Math.sin(radians) * hook.launchSpeed
    };
    
    console.log(`钩子发射角度: ${hook.currentAngle}°, 速度: (${hook.velocity.x}, ${hook.velocity.y})`);
  }

  execute(hook: HookStateMachine): void {
    // 更新钩子位置
    hook.hookPosition.x += hook.velocity.x;
    hook.hookPosition.y += hook.velocity.y;
    
    // 应用重力
    hook.velocity.y += hook.gravity;
    
    // 检测碰撞
    const collisionItem = hook.checkCollision();
    if (collisionItem) {
      hook.caughtItem = collisionItem;
      hook.changeState(HookState.GRABBING);
      return;
    }
    
    // 检测是否超出最大距离
    const distanceFromBase = Math.sqrt(
      Math.pow(hook.hookPosition.x - hook.baseX, 2) + 
      Math.pow(hook.hookPosition.y - hook.baseY, 2)
    );
    
    if (distanceFromBase > hook.maxDistance) {
      // 钩子达到最大距离，开始回收
      hook.changeState(HookState.RETRIEVING);
    }
  }

  exit(hook: HookStateMachine): void {
    console.log('钩子退出发射状态');
    hook.isLaunched = false;
  }
}

// 回收状态
class RetrievingState implements IHookState {
  enter(hook: HookStateMachine): void {
    console.log('钩子进入回收状态');
    // 如果没有抓到物品，则设置为空气
    if (!hook.caughtItem) {
      hook.caughtItem = new GrabbableItem(GrabbableItemType.EMPTY, 0, 0);
    }
  }

  execute(hook: HookStateMachine): void {
    // 计算返回基础位置的方向向量
    const dx = hook.baseX - hook.hookPosition.x;
    const dy = hook.baseY - hook.hookPosition.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    if (distance < 5) { // 接近基础位置
      // 处理抓取结果
      if (hook.caughtItem && hook.caughtItem.type !== GrabbableItemType.EMPTY) {
        if (hook.caughtItem.type === GrabbableItemType.GOLD) {
          console.log(`成功抓取金块！获得价值 ${hook.caughtItem.value}`);
          hook.score += hook.caughtItem.value;
        } else if (hook.caughtItem.type === GrabbableItemType.STONE) {
          console.log(`钩到石头！重量: ${hook.caughtItem.weight}`);
          // 石头太重，可能会影响钩子
          if (hook.caughtItem.weight > hook.maxWeightCapacity) {
            console.log('石头太重，钩子断了！');
            hook.reset(); // 重置钩子
            return;
          }
        }
      } else {
        console.log('钩子空手而归');
      }
      
      // 清除捕获的物品
      hook.caughtItem = null;
      
      // 返回待命状态
      hook.changeState(HookState.IDLE);
      return;
    }
    
    // 向基础位置移动
    const speed = 8; // 回收速度
    const moveX = (dx / distance) * speed;
    const moveY = (dy / distance) * speed;
    
    hook.hookPosition.x += moveX;
    hook.hookPosition.y += moveY;
  }

  exit(hook: HookStateMachine): void {
    console.log('钩子退出回收状态');
  }
}

// 抓取状态
class GrabbingState implements IHookState {
  private grabTimer: number = 0;
  private maxGrabTime: number = 30; // 最大抓取时间（帧数）
  
  enter(hook: HookStateMachine): void {
    console.log('钩子进入抓取状态');
    this.grabTimer = 0;
    
    if (hook.caughtItem) {
      console.log(`钩到了: ${hook.caughtItem.type}, 重量: ${hook.caughtItem.weight}, 价值: ${hook.caughtItem.value}`);
      
      // 如果钩到石头且太重，可能导致失败
      if (hook.caughtItem.type === GrabbableItemType.STONE && 
          hook.caughtItem.weight > hook.maxWeightCapacity) {
        console.log('石头太重，抓取失败！');
        hook.caughtItem = null;
        hook.changeState(HookState.RETRIEVING);
        return;
      }
    }
  }

  execute(hook: HookStateMachine): void {
    this.grabTimer++;
    
    // 模拟抓取动画
    // 实际游戏中这里会有视觉反馈
    
    // 检查是否完成抓取
    if (this.grabTimer >= this.maxGrabTime) {
      hook.changeState(HookState.RETRIEVING);
    }
  }

  exit(hook: HookStateMachine): void {
    console.log('钩子退出抓取状态');
  }
}

// 钩子状态机主类
class HookStateMachine {
  // 钩子属性
  baseX: number = 400;  // 钩子基座 X 坐标
  baseY: number = 100;  // 钩子基座 Y 坐标
  initialAngle: number = 0;  // 初始角度
  currentAngle: number = 0;  // 当前角度
  launchSpeed: number = 8;   // 发射速度
  gravity: number = 0.3;     // 重力加速度
  maxDistance: number = 300; // 最大距离
  maxWeightCapacity: number = 15; // 最大承重能力
  score: number = 0;         // 玩家得分
  
  // 钩子状态
  currentState: IHookState;
  stateEnum: HookState;
  hookPosition: { x: number; y: number };
  velocity: { x: number; y: number };
  isSwinging: boolean = false;
  isLaunched: boolean = false;
  caughtItem: GrabbableItem | null = null;
  
  // 输入控制
  shouldLaunch: boolean = false;
  
  // 游戏对象
  gameObjects: GrabbableItem[] = [];
  
  constructor() {
    // 初始化钩子位置
    this.hookPosition = { x: this.baseX, y: this.baseY };
    this.velocity = { x: 0, y: 0 };
    
    // 设置初始状态
    this.stateEnum = HookState.IDLE;
    this.currentState = new IdleState();
    this.currentState.enter(this);
    
    // 创建一些测试物品
    this.createTestItems();
  }
  
  // 创建测试物品
  private createTestItems(): void {
    // 在不同位置放置一些物品
    this.gameObjects.push(new GrabbableItem(GrabbableItemType.GOLD, 5, 100));
    this.gameObjects.push(new GrabbableItem(GrabbableItemType.STONE, 20, 10));
    this.gameObjects.push(new GrabbableItem(GrabbableItemType.GOLD, 8, 150));
    this.gameObjects.push(new GrabbableItem(GrabbableItemType.STONE, 25, 5));
  }
  
  // 改变状态
  changeState(newState: HookState): void {
    // 退出当前状态
    this.currentState.exit(this);
    
    // 设置新状态
    this.stateEnum = newState;
    
    switch (newState) {
      case HookState.IDLE:
        this.currentState = new IdleState();
        break;
      case HookState.SWINGING:
        this.currentState = new SwingingState();
        break;
      case HookState.LAUNCHING:
        this.currentState = new LaunchingState();
        break;
      case HookState.RETRIEVING:
        this.currentState = new RetrievingState();
        break;
      case HookState.GRABBING:
        this.currentState = new GrabbingState();
        break;
      default:
        this.currentState = new IdleState();
        break;
    }
    
    // 进入新状态
    this.currentState.enter(this);
  }
  
  // 更新钩子位置
  updateHookPosition(): void {
    const radians = this.currentAngle * Math.PI / 180;
    this.hookPosition = {
      x: this.baseX + Math.cos(radians) * 50, // 50是摆动半径
      y: this.baseY + Math.sin(radians) * 50
    };
  }
  
  // 检测碰撞
  checkCollision(): GrabbableItem | null {
    // 这里简化处理，实际游戏中需要精确的碰撞检测
    // 模拟检测是否钩到了某个物品
    for (let i = 0; i < this.gameObjects.length; i++) {
      const item = this.gameObjects[i];
      // 简化的碰撞检测逻辑
      const distance = Math.sqrt(
        Math.pow(this.hookPosition.x - (Math.random() * 800), 2) + 
        Math.pow(this.hookPosition.y - (Math.random() * 600), 2)
      );
      
      // 随机模拟是否钩到物品（在实际实现中，这里应该是精确的碰撞检测）
      if (Math.random() > 0.95) { // 5% 的概率钩到物品
        const randomIndex = Math.floor(Math.random() * this.gameObjects.length);
        const grabbedItem = this.gameObjects[randomIndex];
        // 从游戏中移除被抓取的物品
        this.gameObjects.splice(randomIndex, 1);
        return grabbedItem;
      }
    }
    
    return null;
  }
  
  // 重置钩子
  reset(): void {
    this.caughtItem = null;
    this.changeState(HookState.IDLE);
  }
  
  // 更新状态机
  update(): void {
    this.currentState.execute(this);
  }
  
  // 发射钩子
  launch(): void {
    this.shouldLaunch = true;
  }
  
  // 重置发射标志
  resetLaunch(): void {
    this.shouldLaunch = false;
  }
  
  // 获取当前状态字符串
  getStateString(): string {
    return this.stateEnum;
  }
}

// 使用示例和测试
function runDemo() {
  console.log('=== 黄金矿工钩子状态机演示 ===\n');
  
  const hook = new HookStateMachine();
  
  // 模拟游戏循环
  let frameCount = 0;
  const maxFrames = 100;
  
  console.log('初始状态:', hook.getStateString());
  
  while (frameCount < maxFrames) {
    frameCount++;
    console.log(`\n--- 帧 ${frameCount} ---`);
    console.log('当前状态:', hook.getStateString());
    console.log(`钩子位置: (${hook.hookPosition.x.toFixed(2)}, ${hook.hookPosition.y.toFixed(2)})`);
    
    // 模拟游戏逻辑
    if (frameCount === 5) {
      console.log('\n-> 玩家按下发射按钮');
      hook.launch();
    }
    
    if (frameCount === 15 && hook.stateEnum === HookState.SWINGING) {
      console.log('\n-> 玩家在摆动时发射');
      hook.launch();
    }
    
    // 更新状态机
    hook.update();
    
    // 重置发射标志（在实际游戏中，这是由玩家控制的）
    if (frameCount % 10 === 0) {
      hook.resetLaunch();
    }
    
    // 显示分数
    if (hook.score > 0) {
      console.log(`当前得分: ${hook.score}`);
    }
    
    // 如果回到IDLE状态，再次发射进行下一轮测试
    if (hook.stateEnum === HookState.IDLE && frameCount > 20) {
      console.log('\n-> 开始新一轮');
      hook.launch();
    }
    
    // 模拟等待状态转换
    if (hook.stateEnum === HookState.IDLE && frameCount > 50) {
      break;
    }
  }
  
  console.log(`\n最终得分: ${hook.score}`);
  console.log('演示结束');
}

// 运行演示
runDemo();

export { 
  HookState, 
  GrabbableItemType, 
  GrabbableItem, 
  HookStateMachine,
  IHookState
};