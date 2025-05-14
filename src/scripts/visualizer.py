import time
import pygame
import torch
import numpy as np

from ray.rllib.algorithms.ppo import PPO

from environment import GridFoodSearchEnv

def visualize_policy(checkpoint_path, env_config, num_episodes=5):
    print(f"\n--- Starting Visualization ---")
    print(f"Loading checkpoint from: {checkpoint_path}")

    try:
        # Restore the Algorithm using the generic base class
        algo = PPO.from_checkpoint(checkpoint_path)
        print("--- DEBUG INFO ---")
        print(f"Checkpoint loaded.")
        print(f"Type of 'algo' object: {type(algo)}")  # Check the type
        print("--------------------")
        print("Algorithm loaded successfully.")
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        return

    # Create the environment instance with render_mode='human'
    vis_env_config = env_config.copy()  # Important: Copy env_config
    vis_env_config["render_mode"] = "human"
    try:
        env = GridFoodSearchEnv(config=vis_env_config)
        print("Environment created for visualization.")
    except Exception as e:
        print(f"Error creating environment: {e}")
        return

    for episode in range(num_episodes):
        print(f"\n--- Starting Visualization Episode {episode + 1}/{num_episodes} ---")
        obs, info = env.reset()
        terminated = {"__all__": False}
        truncated = {"__all__": False}
        step_count = 0
        total_reward_dict = {agent_id: 0.0 for agent_id in env.agents}
        render_active = True

        while not terminated["__all__"] and not truncated["__all__"] and render_active:
            # Render the environment state
            render_result = env.render()

            if render_result is None:  # Check if render signaled exit (window closed)
                print("Render window closed by user.")
                render_active = False
                continue  # Skip rest of the loop for this episode

            time.sleep(0.8)

            try:
                # 1. Get the RL Module (can potentially be moved outside the loop if static)
                module = algo.get_module("shared_policy")
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                module.to(device)
                module.eval()

                # 2. Prepare batch from the observations dictionary
                agent_ids = list(obs.keys())
                if not agent_ids:  # Handle case where obs might be empty temporarily
                    print("Warning: No agents found in observation dict. Skipping step.")
                    time.sleep(0.1)  # Avoid busy-waiting
                    continue

                obs_list = [obs[agent_id] for agent_id in agent_ids]
                obs_batch = np.stack(obs_list, axis=0)

                # Flatten the dictionaries into a NumPy array
                flattened_obs = []
                for obs in obs_batch:
                    # Flatten each observation: agent_position + food_position + terrain
                    flattened = np.concatenate([obs['agent_position'], obs['food_position'], [obs['terrain']]])
                    flattened_obs.append(flattened)

                # Convert to NumPy array with dtype float32
                obs_array = np.array(flattened_obs, dtype=np.float32)

                # Create the input dictionary expected by the RLModule
                input_dict = {
                    "obs": torch.tensor(obs_array, dtype=torch.float32).to(device)
                }

                with torch.no_grad():  # Inference
                    forward_out = module.forward_inference(input_dict)

                # 4. Extract actions
                # Output structure depends on the specific RLModule.
                # Usually a dict containing 'actions', possibly already deterministic.
                action_logits = forward_out.get("action_dist_inputs")

                if action_logits is None:
                    print("Error: Could not find 'action_dist_inputs' in RLModule output.")
                    print("Full module output:", forward_out)
                    break  # Stop episode

                actions_batch_tensor = torch.argmax(action_logits, dim=-1)
                actions_batch = actions_batch_tensor.cpu().numpy()

                # 5. Map batch actions back to agent dictionary
                actions = {agent_ids[i]: int(actions_batch[i]) for i in range(len(agent_ids))}

            except Exception as e:
                print(f"\nError during action computation: {e}")
                import traceback
                traceback.print_exc()
                render_active = False  # Stop visualization on error
                continue  # Skip to next loop iteration or break
            # +++ End: INSERT THE NEW RLModule ACTION COMPUTATION CODE HERE +++

            # Step the environment
            obs, reward, terminated, truncated, info = env.step(actions)
            step_count += 1

            for agent_id, r in reward.items():
                total_reward_dict[agent_id] += r

            # Optional small delay if render FPS isn't enough
            # time.sleep(0.1)

        if render_active:  # Don't print end status if window was closed mid-episode
            print(f"Episode finished after {step_count} steps.")
            print(f"Total rewards: {total_reward_dict}")
            if terminated["__all__"]:
                print("Reason: Food Found (Terminated)")
            elif truncated["__all__"]:
                print("Reason: Max Steps Reached (Truncated)")

            try:
                # Keep showing the last frame and wait for user input
                print("Press Enter to continue to the next episode (or close the window)...")
                # Keep processing events so window doesn't freeze and close button works
                while True:
                    event_processed = False
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            render_active = False
                            event_processed = True
                            break
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:  # Check for Enter key
                                event_processed = True
                                break
                    if event_processed:
                        break  # Exit inner event loop
                    time.sleep(0.05)  # Prevent busy-waiting

                if not render_active:  # If user closed window during pause
                    print("Window closed during pause.")
                    env.close()  # Close immediately if user quit
                    break  # Exit the outer episode loop

            except KeyboardInterrupt:  # Allow Ctrl+C to exit
                render_active = False
                print("\nInterrupted by user.")
                break  # Exit the outer episode loop

        if not render_active:  # Exit outer loop if window was closed
            break

    env.close()  # Clean up the rendering window
    print("\nVisualization finished.")