# 道具与物件状态

## 目录
1. Prop Semantic State
2. Relation Mode
3. Position Zone
4. 连续性与允许变化
5. 交接与易主
6. Failed Prop Action
7. Decision Contact POV
8. 连续道具@绑定

## 1. Prop Semantic State

关键道具内部至少维护：asset_id、holder/fixed_location、hand/contact、relation_mode、position_zone、orientation、functional_state、continuity_active、last_change、next_allowed_change。

## 2. Relation Mode

明确道具与人物/环境关系：`handheld`手持、`worn`佩戴、`hanging`悬挂、`attached`附着、`placed`放置、`pocketed`入袋、`inserted`插入、`mounted`固定安装。容易被模型自动补全的校牌、工牌、耳机、包带、手机链、首饰尤其必须明确relation_mode。

## 3. Position Zone

对会跨镜持续的手持道具维护相对区域，例如`right_shoulder_front`右肩前、`right_ear`右耳、`chest_center`胸前、`waist_side`腰侧、`left_hand_low`左手低位。区域只需可见、可剪辑，不使用厘米级伪精确。

道具从一个position_zone变到另一个必须有可见动作链，不能切镜瞬移。

## 4. 连续性与允许变化

`next_allowed_change`必须有剧情依据，例如“听见小屁孩后手机胸前→右耳”“挂断后手机耳边→胸前”“说完OS后校牌收入掌心”。没有依据时维持上一可见状态。

## 5. 交接与易主

易主必须出现旧持有者→伸手/递出→双方接触→新持有者/新手位→接手反应。镜头切点可发生在接触后，但不能跳过实际交接。

## 6. Failed Prop Action

道具动作也可失败：想挂断但被一句话打断、想藏证据但已被看见、想把手机抬到耳边却孩子先回答。记录动作停在何处，并让下一镜承接该未完成状态。

## 7. Decision Contact POV

按键、签字、删除、解锁、拉门、拿证据等主动选择可以使用Decision Contact POV。必须拍清起始触点、实际接触、功能结果和台词/声音后果。

## 8. 连续道具@绑定

CONTINUITY_PROP可见时在该镜@对应本地道具图；完全裁出画面时不强塞。跨段Semantic ID稳定，本地`@[图片N]`每段重新分配。LOCAL_PROP默认不用独立@，除非用户要求锁外观。
